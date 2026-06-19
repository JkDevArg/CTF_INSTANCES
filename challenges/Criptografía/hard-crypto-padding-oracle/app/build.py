import os, secrets, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG  = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')
KEY   = secrets.token_bytes(16)  # fixed per container lifetime
IV    = secrets.token_bytes(16)

cipher     = AES.new(KEY, AES.MODE_CBC, IV)
ciphertext = cipher.encrypt(pad(FLAG.encode(), 16))

os.makedirs('dist', exist_ok=True)

# Save the intercepted ciphertext for the player
data = {
    'iv':         IV.hex(),
    'ciphertext': ciphertext.hex(),
    'oracle':     'POST /oracle  {"iv": "<hex>", "ciphertext": "<hex>"}  → {"valid": true/false}'
}
with open('dist/intercepted.json', 'w') as f:
    json.dump(data, f, indent=2)

# Save KEY for the server to use (the oracle needs it)
with open('/tmp/oracle_key.bin', 'wb') as f:
    f.write(KEY)
