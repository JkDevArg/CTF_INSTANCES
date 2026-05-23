import asyncio
from app.docker_manager import get_docker_manager
from app.flag_manager import get_flag_manager

async def test():
    dm = get_docker_manager()
    await dm.initialize()
    fm = get_flag_manager()
    print("challenge_mapping:", fm.challenge_mapping)
    print("challenges:", list(dm.challenges.keys()))
    res = dm.resolve_challenge_id("2")
    print("resolved:", res)

asyncio.run(test())
