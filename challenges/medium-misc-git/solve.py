"""
Solución: medium-misc-git

1. Descargar corp-repo.bundle desde http://<host>/files/corp-repo.bundle
2. Clonar: git clone corp-repo.bundle corp-repo
3. Ver historial: git -C corp-repo log --oneline
4. El commit "fix: add backup configuration" contiene la flag
5. git -C corp-repo show <hash>:config.py
   o bien: git -C corp-repo log -p | grep BACKUP_KEY
"""
import subprocess, re, os, sys

BUNDLE = 'corp-repo.bundle'
REPO   = 'corp-repo'

if not os.path.exists(BUNDLE):
    print(f"[-] Descarga primero el bundle: wget http://<host>/files/{BUNDLE}")
    sys.exit(1)

if not os.path.exists(REPO):
    subprocess.run(['git', 'clone', BUNDLE, REPO], check=True)

result = subprocess.run(
    ['git', '-C', REPO, 'log', '-p', '--all'],
    capture_output=True, text=True
)

match = re.search(r'\+BACKUP_KEY = "(.+)"', result.stdout)
if match:
    print(f"[+] FLAG: {match.group(1)}")
else:
    print("[-] Flag no encontrada — revisa el log manualmente:")
    print(result.stdout[:2000])
