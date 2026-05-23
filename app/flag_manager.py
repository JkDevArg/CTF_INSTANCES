"""Dynamic flag management for CTFd integration."""
import json
import secrets
import httpx
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from threading import Lock
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

from .config import settings
from .logger import event_logger


@dataclass
class FlagMapping:
    """Represents a flag assigned to a user/team for a challenge."""
    flag_id: int  # CTFd flag ID
    ctfd_challenge_id: int  # CTFd challenge ID
    local_challenge_id: str  # Our local challenge ID
    user_id: str
    username: str
    flag_content: str
    created_at: str
    instance_id: Optional[str] = None
    # Team mode fields
    team_id: Optional[str] = None
    team_name: Optional[str] = None
    owner_id: Optional[str] = None  # user_id in user mode, team_id in team mode


@dataclass
class SuspiciousSubmission:
    """A submission where user submitted someone else's flag."""
    submission_id: int
    submitter_user_id: int
    submitter_username: str
    flag_owner_user_id: str
    flag_owner_username: str
    challenge_id: int
    local_challenge_id: str
    provided_flag: str
    submission_time: str
    ip_address: str
    # Team mode fields (populated when team mode is enabled)
    submitter_team_id: Optional[str] = None
    submitter_team_name: Optional[str] = None
    flag_owner_team_id: Optional[str] = None
    flag_owner_team_name: Optional[str] = None


class FlagManager:
    """Manages dynamic flags for anti-cheat functionality."""
    
    def __init__(self, persist_file: str = "/app/logs/flag_mappings.json"):
        self.persist_file = Path(persist_file)
        self._lock = Lock()
        
        # flag_id -> FlagMapping
        self.flag_mappings: Dict[int, FlagMapping] = {}
        
        # user_id -> {local_challenge_id -> flag_id}
        self.user_flags: Dict[str, Dict[str, int]] = {}
        
        # owner_id -> {local_challenge_id -> flag_id}
        # In user mode: owner_id = user_id
        # In team mode: owner_id = team_id
        self.owner_flags: Dict[str, Dict[str, int]] = {}
        
        # flag_content -> flag_id (for quick lookup)
        self.flag_lookup: Dict[str, int] = {}
        
        # CTFd challenge mapping: local_challenge_id -> ctfd_challenge_id
        self.challenge_mapping: Dict[str, int] = {}
        
        # Suspicious submissions found
        self.suspicious_submissions: List[SuspiciousSubmission] = []
        
        self._load_mappings()
    
    def _load_mappings(self) -> None:
        """Load persisted flag mappings from file."""
        try:
            if self.persist_file.exists():
                with open(self.persist_file, 'r') as f:
                    data = json.load(f)

                    # Load flag mappings
                    for flag_id_str, mapping_data in data.get("flag_mappings", {}).items():
                        flag_id = int(flag_id_str)
                        # Normalize stored IDs to str
                        mapping_data["user_id"] = str(mapping_data.get("user_id", ""))
                        if mapping_data.get("team_id") is not None:
                            mapping_data["team_id"] = str(mapping_data["team_id"])
                        if mapping_data.get("owner_id") is not None:
                            mapping_data["owner_id"] = str(mapping_data["owner_id"])
                        mapping = FlagMapping(**mapping_data)
                        self.flag_mappings[flag_id] = mapping
                        self.flag_lookup[mapping.flag_content] = flag_id

                    # Load user_flags index — normalize keys to str
                    raw_user_flags = data.get("user_flags", {})
                    self.user_flags = {str(k): v for k, v in raw_user_flags.items()}

                    # Load owner_flags index (for team mode) — normalize keys to str
                    raw_owner_flags = data.get("owner_flags", {})
                    self.owner_flags = {str(k): v for k, v in raw_owner_flags.items()}

                    # Load challenge mapping
                    self.challenge_mapping = data.get("challenge_mapping", {})

                    # Load suspicious submissions
                    for sub_data in data.get("suspicious_submissions", []):
                        self.suspicious_submissions.append(SuspiciousSubmission(**sub_data))

                print(f"Loaded {len(self.flag_mappings)} flag mappings, {len(self.challenge_mapping)} challenge mappings")
                if self.challenge_mapping:
                    print(f"Challenge mappings: {self.challenge_mapping}")
        except Exception as e:
            print(f"Failed to load flag mappings: {e}")
    
    def _save_mappings(self) -> None:
        """Persist flag mappings to file."""
        try:
            self.persist_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "flag_mappings": {
                    str(k): asdict(v) for k, v in self.flag_mappings.items()
                },
                "user_flags": self.user_flags,
                "owner_flags": self.owner_flags,
                "challenge_mapping": self.challenge_mapping,
                "suspicious_submissions": [asdict(s) for s in self.suspicious_submissions]
            }
            
            with open(self.persist_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save flag mappings: {e}")
    
    def generate_flag(self, prefix: str = "FLAG") -> str:
        """Generate a unique random flag."""
        random_part = secrets.token_hex(16)
        return f"{prefix}{{{random_part}}}"
    
    async def get_ctfd_challenge_id(self, local_challenge_id: str) -> Optional[int]:
        """
        Get CTFd challenge ID from saved mapping.
        Mappings are set manually via admin panel.
        """
        # Check cache first (exact match)
        if local_challenge_id in self.challenge_mapping:
            print(f"Found mapping: {local_challenge_id} -> {self.challenge_mapping[local_challenge_id]}")
            return self.challenge_mapping[local_challenge_id]
        
        # Try case-insensitive lookup in existing mappings
        for key, value in self.challenge_mapping.items():
            if key.lower() == local_challenge_id.lower():
                print(f"Found case-insensitive mapping: {key} -> {value}")
                return value
        
        # Try reloading from disk in case it was updated via admin panel
        self._load_mappings()
        
        if local_challenge_id in self.challenge_mapping:
            print(f"Found mapping after reload: {local_challenge_id} -> {self.challenge_mapping[local_challenge_id]}")
            return self.challenge_mapping[local_challenge_id]
        
        # Case-insensitive check after reload
        for key, value in self.challenge_mapping.items():
            if key.lower() == local_challenge_id.lower():
                print(f"Found case-insensitive mapping after reload: {key} -> {value}")
                return value
        
        # No mapping found - user needs to set it via admin panel
        print(f"No CTFd mapping for '{local_challenge_id}'. Please set it via Admin Panel -> Dynamic Flags -> Challenge ID Mapping")
        print(f"Current mappings: {self.challenge_mapping}")
        return None
    
    async def create_flag_for_user(
        self,
        local_challenge_id: str,
        user_id: str,
        username: str,
        instance_id: str
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Create a unique flag for a user and register it with CTFd.
        Returns (success, message, flag_content).
        """
        if not settings.CTFD_URL or not settings.CTFD_API_KEY:
            return False, "CTFd not configured", None

        # Always normalize IDs to str to prevent int/str key collisions
        user_id = str(user_id)

        # Check if user already has a flag for this challenge
        existing_flag_id = self.user_flags.get(user_id, {}).get(local_challenge_id)
        if existing_flag_id and existing_flag_id in self.flag_mappings:
            # Return existing flag
            existing = self.flag_mappings[existing_flag_id]
            print(f"[flag_manager] Reusing existing flag for user {username} on {local_challenge_id}")
            return True, "Using existing flag", existing.flag_content

        # Get CTFd challenge ID
        ctfd_challenge_id = await self.get_ctfd_challenge_id(local_challenge_id)
        if not ctfd_challenge_id:
            return False, f"Challenge '{local_challenge_id}' not found in CTFd", None
        
        # Generate unique flag with configured prefix
        flag_content = self.generate_flag(prefix=settings.FLAG_PREFIX)
        
        try:
            async with httpx.AsyncClient() as client:
                # Create flag in CTFd
                response = await client.post(
                    f"{settings.CTFD_URL}/api/v1/flags",
                    headers={
                        "Authorization": f"Token {settings.CTFD_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "challenge_id": ctfd_challenge_id,
                        "type": "static",
                        "content": flag_content,
                        "data": f"user:{user_id}|username:{username}|instance:{instance_id}"
                    },
                    timeout=10.0
                )
                
                if response.status_code in (200, 201):
                    data = response.json()
                    if data.get("success"):
                        flag_id = data["data"]["id"]
                        
                        # Save mapping
                        with self._lock:
                            mapping = FlagMapping(
                                flag_id=flag_id,
                                ctfd_challenge_id=ctfd_challenge_id,
                                local_challenge_id=local_challenge_id,
                                user_id=user_id,
                                username=username,
                                flag_content=flag_content,
                                created_at=datetime.now(timezone.utc).isoformat(),
                                instance_id=instance_id
                            )
                            
                            self.flag_mappings[flag_id] = mapping
                            self.flag_lookup[flag_content] = flag_id
                            
                            if user_id not in self.user_flags:
                                self.user_flags[user_id] = {}
                            self.user_flags[user_id][local_challenge_id] = flag_id
                            
                            self._save_mappings()
                        
                        # Log flag creation event
                        event_logger.log_flag_created(
                            user_id=user_id,
                            username=username,
                            challenge_id=local_challenge_id,
                            flag_id=flag_id,
                            instance_id=instance_id,
                        )
                        
                        print(f"Created flag {flag_id} for user {username} on challenge {local_challenge_id}")
                        return True, "Flag created", flag_content
                    else:
                        return False, f"CTFd error: {data}", None
                else:
                    return False, f"CTFd API error: {response.status_code}", None
                    
        except Exception as e:
            print(f"Error creating flag: {e}")
            return False, f"Error: {str(e)}", None
    
    async def create_flag_for_owner(
        self,
        local_challenge_id: str,
        owner_id: str,
        owner_name: str,
        instance_id: str,
        team_mode: bool = False,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        team_id: Optional[str] = None,
        team_name: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Create a unique flag for an owner (user or team) and register it with CTFd.

        In team mode:
        - owner_id is team_id
        - Flag is shared by all team members
        - user_id/username track who spawned the instance

        In user mode:
        - owner_id is user_id
        - Delegates to create_flag_for_user for backward compatibility

        Returns (success, message, flag_content).
        """
        # Always normalize IDs to str to prevent int/str key collisions
        owner_id = str(owner_id)
        if user_id is not None:
            user_id = str(user_id)
        if team_id is not None:
            team_id = str(team_id)

        if not team_mode:
            # User mode - use existing method for backward compatibility
            return await self.create_flag_for_user(
                local_challenge_id=local_challenge_id,
                user_id=owner_id,
                username=owner_name,
                instance_id=instance_id
            )

        # Team mode
        if not settings.CTFD_URL or not settings.CTFD_API_KEY:
            return False, "CTFd not configured", None

        # Check if team already has a flag for this challenge
        existing_flag_id = self.owner_flags.get(owner_id, {}).get(local_challenge_id)
        if existing_flag_id and existing_flag_id in self.flag_mappings:
            # Return existing team flag
            existing = self.flag_mappings[existing_flag_id]
            print(f"[flag_manager] Reusing existing flag for team {owner_name} on {local_challenge_id}")
            return True, "Using existing team flag", existing.flag_content
        
        # Get CTFd challenge ID
        ctfd_challenge_id = await self.get_ctfd_challenge_id(local_challenge_id)
        if not ctfd_challenge_id:
            return False, f"Challenge '{local_challenge_id}' not found in CTFd", None
        
        # Generate unique flag with configured prefix
        flag_content = self.generate_flag(prefix=settings.FLAG_PREFIX)
        
        try:
            async with httpx.AsyncClient() as client:
                # Create flag in CTFd with team info
                response = await client.post(
                    f"{settings.CTFD_URL}/api/v1/flags",
                    headers={
                        "Authorization": f"Token {settings.CTFD_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "challenge_id": ctfd_challenge_id,
                        "type": "static",
                        "content": flag_content,
                        "data": f"team:{team_id}|team_name:{team_name}|spawned_by:{username}|instance:{instance_id}"
                    },
                    timeout=10.0
                )
                
                if response.status_code in (200, 201):
                    data = response.json()
                    if data.get("success"):
                        flag_id = data["data"]["id"]
                        
                        # Save mapping with team info
                        with self._lock:
                            mapping = FlagMapping(
                                flag_id=flag_id,
                                ctfd_challenge_id=ctfd_challenge_id,
                                local_challenge_id=local_challenge_id,
                                user_id=user_id or owner_id,
                                username=username or owner_name,
                                flag_content=flag_content,
                                created_at=datetime.now(timezone.utc).isoformat(),
                                instance_id=instance_id,
                                team_id=team_id,
                                team_name=team_name,
                                owner_id=owner_id
                            )
                            
                            self.flag_mappings[flag_id] = mapping
                            self.flag_lookup[flag_content] = flag_id
                            
                            # Update owner_flags index (for team mode lookups)
                            if owner_id not in self.owner_flags:
                                self.owner_flags[owner_id] = {}
                            self.owner_flags[owner_id][local_challenge_id] = flag_id
                            
                            # Also update user_flags for backward compatibility
                            if user_id:
                                if user_id not in self.user_flags:
                                    self.user_flags[user_id] = {}
                                self.user_flags[user_id][local_challenge_id] = flag_id
                            
                            self._save_mappings()
                        
                        # Log flag creation event
                        event_logger.log_flag_created(
                            user_id=user_id or owner_id,
                            username=username or owner_name,
                            challenge_id=local_challenge_id,
                            flag_id=flag_id,
                            instance_id=instance_id,
                            extra={"team_id": team_id, "team_name": team_name, "team_mode": True}
                        )
                        
                        print(f"Created flag {flag_id} for team {team_name} on challenge {local_challenge_id}")
                        return True, "Flag created", flag_content
                    else:
                        return False, f"CTFd error: {data}", None
                else:
                    return False, f"CTFd API error: {response.status_code}", None
                    
        except Exception as e:
            print(f"Error creating team flag: {e}")
            return False, f"Error: {str(e)}", None
    
    async def delete_flag(self, flag_id: int) -> bool:
        """Delete a flag from CTFd."""
        if not settings.CTFD_URL or not settings.CTFD_API_KEY:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{settings.CTFD_URL}/api/v1/flags/{flag_id}",
                    headers={
                        "Authorization": f"Token {settings.CTFD_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=10.0
                )
                
                return response.status_code in (200, 204)
        except Exception as e:
            print(f"Error deleting flag {flag_id}: {e}")
            return False

    async def has_solved_challenge(self, challenge_id: int, user_id: str, team_id: Optional[str] = None, team_mode: bool = False) -> bool:
        """Check if a user or team has already solved the challenge in CTFd."""
        if not settings.CTFD_URL or not settings.CTFD_API_KEY:
            return False
            
        try:
            # En CTFd la forma más fácil de ver si un equipo/usuario resolvió algo como admin
            # es consultar los solves del equipo o usuario
            target_type = "teams" if team_mode and team_id else "users"
            target_id = team_id if team_mode and team_id else user_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.CTFD_URL}/api/v1/{target_type}/{target_id}/solves",
                    headers={
                        "Authorization": f"Token {settings.CTFD_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        solves = data.get("data", [])
                        for solve in solves:
                            if solve.get("challenge_id") == challenge_id:
                                return True
        except Exception as e:
            print(f"[flag_manager] Error checking solve status: {e}")
            
        return False

    async def cleanup_instance_flag(self, local_challenge_id: str, user_id: str, team_id: Optional[str] = None, team_mode: bool = False) -> bool:
        """
        Delete the flag generated for a specific challenge and user/team,
        but ONLY if they haven't already solved the challenge.
        """
        owner_id = str(team_id) if team_mode and team_id else str(user_id)
        
        # Check if they have a flag mapped
        flag_id = self.owner_flags.get(owner_id, {}).get(local_challenge_id)
        if not flag_id:
            return False
            
        mapping = self.flag_mappings.get(flag_id)
        if not mapping:
            return False
            
        # Check if they have solved it
        has_solved = await self.has_solved_challenge(
            challenge_id=mapping.ctfd_challenge_id,
            user_id=str(user_id),
            team_id=str(team_id) if team_id else None,
            team_mode=team_mode
        )
        
        if has_solved:
            print(f"[flag_manager] Keeping flag {flag_id} because owner {owner_id} already solved challenge {local_challenge_id}")
            return False
            
        print(f"[flag_manager] Deleting flag {flag_id} because owner {owner_id} hasn't solved {local_challenge_id} yet")
        if await self.delete_flag(flag_id):
            # Remove from mappings
            with self._lock:
                flag_content = mapping.flag_content
                if flag_id in self.flag_mappings:
                    del self.flag_mappings[flag_id]
                if flag_content in self.flag_lookup:
                    del self.flag_lookup[flag_content]
                if owner_id in self.owner_flags and local_challenge_id in self.owner_flags[owner_id]:
                    del self.owner_flags[owner_id][local_challenge_id]
                if user_id in self.user_flags and local_challenge_id in self.user_flags[user_id]:
                    del self.user_flags[user_id][local_challenge_id]
                
            self._save_mappings()
            return True
            
        return False
    
    async def check_submissions(self, limit: int = 150) -> List[SuspiciousSubmission]:
        """
        Check recent submissions for cheating (submitting someone else's flag).
        Checks ALL submissions (not just correct ones) to catch any attempt to use stolen flags.
        Returns list of suspicious submissions found.
        """
        if not settings.CTFD_URL or not settings.CTFD_API_KEY:
            print("[check_submissions] CTFd not configured")
            return []
        
        # Debug: show current flag mappings count
        print(f"[check_submissions] Checking with {len(self.flag_lookup)} flags in lookup table")
        if self.flag_lookup:
            # Show first few flag prefixes for debugging (truncated for security)
            sample_flags = list(self.flag_lookup.keys())[:3]
            print(f"[check_submissions] Sample flag prefixes: {[f[:15]+'...' for f in sample_flags]}")
        
        new_suspicious = []
        
        try:
            async with httpx.AsyncClient() as client:
                # First, get total pages - fetch ALL submissions (not just correct)
                response = await client.get(
                    f"{settings.CTFD_URL}/api/v1/submissions",
                    headers={
                        "Authorization": f"Token {settings.CTFD_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    params={
                        "per_page": 50,
                        "page": 1
                    },
                    timeout=15.0
                )
                
                if response.status_code != 200:
                    print(f"[check_submissions] Failed to fetch submissions: {response.status_code}")
                    return []
                
                data = response.json()
                if not data.get("success"):
                    print(f"[check_submissions] API returned success=false")
                    return []
                
                # Get pagination info
                meta = data.get("meta", {}).get("pagination", {})
                total_pages = meta.get("pages", 1)
                total_submissions = meta.get("total", 0)
                per_page = meta.get("per_page", 50)
                
                print(f"[check_submissions] Total submissions in CTFd: {total_submissions}, pages: {total_pages}")
                
                # Fetch latest pages (work backwards from last page)
                all_submissions = []
                pages_to_fetch = min(5, total_pages)  # Fetch last 5 pages max (250 submissions)
                
                for page_num in range(total_pages, max(total_pages - pages_to_fetch, 0), -1):
                    page_response = await client.get(
                        f"{settings.CTFD_URL}/api/v1/submissions",
                        headers={
                            "Authorization": f"Token {settings.CTFD_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        params={
                            "per_page": per_page,
                            "page": page_num
                        },
                        timeout=15.0
                    )
                    
                    if page_response.status_code == 200:
                        page_data = page_response.json()
                        if page_data.get("success"):
                            page_submissions = page_data.get("data", [])
                            all_submissions.extend(page_submissions)
                            print(f"[check_submissions] Fetched page {page_num}: {len(page_submissions)} submissions")
                
                submissions = all_submissions[:limit]  # Limit total
                print(f"[check_submissions] Processing {len(submissions)} submissions")
                
                # Get user info for lookups
                users_cache = {}
                matched_flags = 0
                
                for sub in submissions:
                    provided_flag = sub.get("provided", "")
                    submitter_user_id = str(sub.get("user_id", ""))  # normalize to str
                    challenge_id = sub.get("challenge_id")
                    submission_id = sub.get("id")
                    submission_type = sub.get("type", "unknown")
                    
                    # Check if this flag belongs to a different user
                    if provided_flag in self.flag_lookup:
                        matched_flags += 1
                        flag_id = self.flag_lookup[provided_flag]
                        flag_mapping = self.flag_mappings.get(flag_id)
                        
                        if flag_mapping:
                            # In team mode, compare by team_id
                            # In user mode, compare by user_id
                            flag_owner_team_id = flag_mapping.team_id
                            flag_owner_user_id = flag_mapping.user_id
                            
                            # Get submitter info from submission data
                            # API format: {"user": {"name": "x", "id": 1}, "team": {"name": "y", "id": 2}, "team_id": 2, "user_id": 1}
                            submitter_username = None
                            submitter_team_id = None
                            submitter_team_name = None
                            
                            # Extract user info
                            if "user" in sub and sub["user"]:
                                submitter_username = sub["user"].get("name")
                            
                            # Extract team info - in team mode, "team" object and "team_id" are present
                            if "team" in sub and sub["team"]:
                                submitter_team_id = str(sub["team"].get("id")) if sub["team"].get("id") is not None else None
                                submitter_team_name = sub["team"].get("name")
                            elif sub.get("team_id"):
                                # Fallback: team_id without team object
                                submitter_team_id = str(sub.get("team_id"))
                            
                            # Fallback to API if not in submission data
                            if not submitter_username or (flag_owner_team_id and not submitter_team_id):
                                if submitter_user_id not in users_cache:
                                    user_resp = await client.get(
                                        f"{settings.CTFD_URL}/api/v1/users/{submitter_user_id}",
                                        headers={
                                            "Authorization": f"Token {settings.CTFD_API_KEY}",
                                            "Content-Type": "application/json"
                                        },
                                        timeout=5.0
                                    )
                                    if user_resp.status_code == 200:
                                        user_data = user_resp.json()
                                        if user_data.get("success"):
                                            users_cache[submitter_user_id] = {
                                                "name": user_data["data"].get("name", str(submitter_user_id)),
                                                "team_id": user_data["data"].get("team_id")
                                            }
                                    else:
                                        users_cache[submitter_user_id] = {"name": str(submitter_user_id), "team_id": None}
                                
                                cached = users_cache.get(submitter_user_id, {})
                                if not submitter_username:
                                    submitter_username = cached.get("name", str(submitter_user_id))
                                if not submitter_team_id:
                                    raw_tid = cached.get("team_id")
                                    submitter_team_id = str(raw_tid) if raw_tid is not None else None
                            
                            # Determine if suspicious based on mode
                            is_suspicious = False
                            comparison_msg = ""
                            
                            if flag_owner_team_id:
                                # Team mode: compare by team_id
                                if submitter_team_id and str(submitter_team_id) != str(flag_owner_team_id):
                                    is_suspicious = True
                                    comparison_msg = f"Team {submitter_team_id} submitted flag belonging to Team {flag_owner_team_id}"
                                elif not submitter_team_id and str(submitter_user_id) != str(flag_owner_user_id):
                                    # Submitter has no team but flag owner does - suspicious
                                    is_suspicious = True
                                    comparison_msg = f"User {submitter_username} (no team) submitted team flag"
                            else:
                                # User mode: compare by user_id
                                if str(submitter_user_id) != str(flag_owner_user_id):
                                    is_suspicious = True
                                    comparison_msg = f"User {submitter_username} submitted flag belonging to {flag_mapping.username}"
                            
                            if is_suspicious:
                                # Get submitter team name from API if not already available from submission
                                if submitter_team_id and not submitter_team_name:
                                    try:
                                        team_resp = await client.get(
                                            f"{settings.CTFD_URL}/api/v1/teams/{submitter_team_id}",
                                            headers={
                                                "Authorization": f"Token {settings.CTFD_API_KEY}",
                                                "Content-Type": "application/json"
                                            },
                                            timeout=5.0
                                        )
                                        if team_resp.status_code == 200:
                                            team_data = team_resp.json()
                                            if team_data.get("success"):
                                                submitter_team_name = team_data["data"].get("name")
                                    except:
                                        pass
                                
                                print(f"[check_submissions] SUSPICIOUS: {comparison_msg} | Submitter: {submitter_username} (Team: {submitter_team_name}) | Flag Owner Team: {flag_mapping.team_name}")
                                
                                suspicious = SuspiciousSubmission(
                                    submission_id=submission_id,
                                    submitter_user_id=submitter_user_id,
                                    submitter_username=submitter_username,
                                    flag_owner_user_id=flag_owner_user_id,
                                    flag_owner_username=flag_mapping.username,
                                    challenge_id=challenge_id,
                                    local_challenge_id=flag_mapping.local_challenge_id,
                                    provided_flag=provided_flag[:20] + "...",  # Truncate for security
                                    submission_time=sub.get("date", ""),
                                    ip_address=sub.get("ip", "unknown"),
                                    # Team info
                                    submitter_team_id=str(submitter_team_id) if submitter_team_id else None,
                                    submitter_team_name=submitter_team_name,
                                    flag_owner_team_id=flag_owner_team_id,
                                    flag_owner_team_name=flag_mapping.team_name
                                )
                                
                                # Check if already recorded
                                existing_ids = {s.submission_id for s in self.suspicious_submissions}
                                if submission_id not in existing_ids:
                                    new_suspicious.append(suspicious)
                                    self.suspicious_submissions.append(suspicious)
                                    
                                    # Log to event logger
                                    event_logger.log_suspicious_submission(
                                        submitter_user_id=str(submitter_user_id),
                                        submitter_username=submitter_username,
                                        flag_owner_user_id=str(flag_owner_user_id),
                                        flag_owner_username=flag_mapping.username,
                                        challenge_id=str(challenge_id),
                                        local_challenge_id=flag_mapping.local_challenge_id,
                                        submission_id=submission_id,
                                        ip_address=sub.get("ip", "unknown"),
                                        extra={
                                            "submitter_team_id": submitter_team_id,
                                            "submitter_team_name": submitter_team_name,
                                            "flag_owner_team_id": flag_owner_team_id,
                                            "flag_owner_team_name": flag_mapping.team_name,
                                            "provided_flag": provided_flag[:20] + "..."
                                        }
                                    )
                                    
                                    # Auto-Delete Cheats
                                    if settings.AUTO_DELETE_CHEATS:
                                        print(f"[check_submissions] Auto-deleting suspicious submission {submission_id} from CTFd...")
                                        try:
                                            del_resp = await client.delete(
                                                f"{settings.CTFD_URL}/api/v1/submissions/{submission_id}",
                                                headers={
                                                    "Authorization": f"Token {settings.CTFD_API_KEY}",
                                                    "Content-Type": "application/json"
                                                },
                                                timeout=10.0
                                            )
                                            if del_resp.status_code in (200, 204, 202):
                                                print(f"[check_submissions] Successfully deleted submission {submission_id}")
                                            else:
                                                print(f"[check_submissions] Failed to delete submission {submission_id}: {del_resp.status_code}")
                                        except Exception as e:
                                            print(f"[check_submissions] Error auto-deleting submission {submission_id}: {e}")
                                    
                                    # Force Stop Cheater's Instance
                                    if settings.STOP_INSTANCE_ON_CHEAT:
                                        try:
                                            from .docker_manager import get_docker_manager
                                            dm = get_docker_manager()
                                            
                                            # Find running instances for the submitter and this challenge
                                            cheater_instances = []
                                            for inst_id, inst in dm.instances.items():
                                                if str(inst.challenge_id) == str(flag_mapping.local_challenge_id):
                                                    # Check if it's the cheater's instance
                                                    is_cheater = False
                                                    if flag_owner_team_id and inst.team_id == submitter_team_id:
                                                        is_cheater = True
                                                    elif not flag_owner_team_id and str(inst.user_id) == str(submitter_user_id):
                                                        is_cheater = True
                                                    
                                                    if is_cheater and inst.status == "running":
                                                        cheater_instances.append(inst_id)
                                            
                                            for inst_id in cheater_instances:
                                                print(f"[check_submissions] Stopping cheater's instance: {inst_id}")
                                                await dm.stop_instance(
                                                    inst_id, 
                                                    terminate_reason="cheat_detected"
                                                )
                                        except Exception as e:
                                            print(f"[check_submissions] Error stopping cheater instance: {e}")
                                    
                                    # Send Discord Alert
                                    if settings.DISCORD_WEBHOOK_URL:
                                        try:
                                            msg = {
                                                "embeds": [{
                                                    "title": "🚨 TRAMPA DETECTADA 🚨",
                                                    "color": 16711680, # Red
                                                    "description": comparison_msg,
                                                    "fields": [
                                                        {"name": "Tramposo", "value": f"{submitter_username} (Team: {submitter_team_name or 'N/A'})", "inline": True},
                                                        {"name": "Víctima (Dueño Real)", "value": f"{flag_mapping.username} (Team: {flag_mapping.team_name or 'N/A'})", "inline": True},
                                                        {"name": "Challenge", "value": f"{flag_mapping.local_challenge_id} (ID: {challenge_id})", "inline": True},
                                                        {"name": "IP Address", "value": sub.get("ip", "unknown"), "inline": True},
                                                        {"name": "Acción", "value": "Envío y puntos ELIMINADOS de CTFd." if settings.AUTO_DELETE_CHEATS else "Registrado para revisión.", "inline": False}
                                                    ],
                                                    "footer": {"text": "Whaley Anti-Cheat System"}
                                                }]
                                            }
                                            await client.post(settings.DISCORD_WEBHOOK_URL, json=msg, timeout=5.0)
                                        except Exception as e:
                                            print(f"[check_submissions] Failed to send Discord alert: {e}")
                            else:
                                if flag_owner_team_id:
                                    print(f"[check_submissions] OK: Team {submitter_team_id} submitted their own flag")
                                else:
                                    print(f"[check_submissions] OK: User {submitter_username} submitted their own flag")
                
                print(f"[check_submissions] Matched {matched_flags} submissions to dynamic flags, found {len(new_suspicious)} new suspicious")
                
                if new_suspicious:
                    self._save_mappings()
                
                return new_suspicious
                
        except Exception as e:
            print(f"[check_submissions] Error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_user_flag(self, user_id: str, local_challenge_id: str) -> Optional[str]:
        """Get the flag content for a user's challenge."""
        # Normalize to str to match stored keys
        flag_id = self.user_flags.get(str(user_id), {}).get(local_challenge_id)
        if flag_id and flag_id in self.flag_mappings:
            return self.flag_mappings[flag_id].flag_content
        return None
    
    def get_all_mappings(self) -> Dict:
        """Get all flag mappings for admin view."""
        return {
            "flag_mappings": [asdict(m) for m in self.flag_mappings.values()],
            "total_flags": len(self.flag_mappings),
            "total_users": len(self.user_flags),
            "suspicious_submissions": [asdict(s) for s in self.suspicious_submissions],
            "challenge_mapping": self.challenge_mapping
        }
    
    def clear_suspicious_submissions(self) -> int:
        """Clear the suspicious submissions list."""
        count = len(self.suspicious_submissions)
        self.suspicious_submissions = []
        self._save_mappings()
        return count
    
    async def cleanup_user_flags(self, user_id: str) -> int:
        """Delete all flags for a user (when cleaning up)."""
        count = 0
        if user_id in self.user_flags:
            for local_challenge_id, flag_id in list(self.user_flags[user_id].items()):
                if await self.delete_flag(flag_id):
                    # Remove from mappings
                    if flag_id in self.flag_mappings:
                        flag_content = self.flag_mappings[flag_id].flag_content
                        del self.flag_mappings[flag_id]
                        if flag_content in self.flag_lookup:
                            del self.flag_lookup[flag_content]
                    count += 1
            
            del self.user_flags[user_id]
            self._save_mappings()
        
        return count


# Global flag manager instance
flag_manager: Optional[FlagManager] = None


def get_flag_manager() -> FlagManager:
    """Get or create the global flag manager."""
    global flag_manager
    if flag_manager is None:
        flag_manager = FlagManager(persist_file=settings.LOG_FILE.replace("events.jsonl", "flag_mappings.json"))
    return flag_manager
