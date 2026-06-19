import os, subprocess, shutil, tempfile

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)

tmp = tempfile.mkdtemp()
try:
    run(['git', 'init', '--initial-branch=main'], cwd=tmp)
    run(['git', 'config', 'user.email', 'dev@corpcorp.local'], cwd=tmp)
    run(['git', 'config', 'user.name', 'dev-bot'], cwd=tmp)

    # Commit 1: initial project
    with open(os.path.join(tmp, 'README.md'), 'w') as f:
        f.write("# CorpCorp Internal Project\n\nVersion 1.0\n")
    with open(os.path.join(tmp, 'config.py'), 'w') as f:
        f.write("DEBUG = False\nHOST = '0.0.0.0'\nPORT = 8080\n")
    run(['git', 'add', '.'], cwd=tmp)
    run(['git', 'commit', '-m', 'feat: initial commit'], cwd=tmp)

    # Commit 2: add credentials (the flag)
    with open(os.path.join(tmp, 'config.py'), 'a') as f:
        f.write(f'\n# Emergency backup key\nBACKUP_KEY = "{FLAG}"\n')
    run(['git', 'add', '.'], cwd=tmp)
    run(['git', 'commit', '-m', 'fix: add backup configuration'], cwd=tmp)

    # Commit 3: remove credentials (too late)
    with open(os.path.join(tmp, 'config.py'), 'w') as f:
        f.write("DEBUG = False\nHOST = '0.0.0.0'\nPORT = 8080\n# backup key removed\n")
    with open(os.path.join(tmp, '.gitignore'), 'w') as f:
        f.write("*.env\n*.key\nsecrets/\n")
    run(['git', 'add', '.'], cwd=tmp)
    run(['git', 'commit', '-m', 'security: remove sensitive data from config'], cwd=tmp)

    # Commit 4: add features
    with open(os.path.join(tmp, 'app.py'), 'w') as f:
        f.write("from config import HOST, PORT\nprint(f'Starting on {HOST}:{PORT}')\n")
    run(['git', 'add', '.'], cwd=tmp)
    run(['git', 'commit', '-m', 'feat: add application entry point'], cwd=tmp)

    os.makedirs('/app/dist', exist_ok=True)
    run(['git', 'bundle', 'create', '/app/dist/corp-repo.bundle', '--all'], cwd=tmp)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
