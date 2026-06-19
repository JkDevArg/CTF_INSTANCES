import os
from rifthash import rifthash

FLAG = os.environ.get('FLAG', 'HL4{143a_chaos}')
SALT = b'unleashed-lab'

hash_str = rifthash(FLAG, SALT)
os.makedirs('dist', exist_ok=True)
with open('dist/rifthash.hash', 'w') as f:
    f.write(hash_str + '\n')
with open('dist/rifthash.py', 'w') as f:
    f.write(open('rifthash.py').read())
print(f'[build] rifthash.hash generado')
