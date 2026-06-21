import os
from rifthash2 import rifthash2

FLAG = os.environ.get('FLAG', 'HL4{SFD_111_Body_Rare_Spell}')
SALT = b'ogs-sfd-unl'

hash_str = rifthash2(FLAG, SALT)
os.makedirs('dist', exist_ok=True)
with open('dist/rifthash2.hash', 'w') as f:
    f.write(hash_str + '\n')
with open('dist/rifthash2.py', 'w') as f:
    f.write(open('rifthash2.py').read())
print(f'[build] rifthash2.hash generado')
