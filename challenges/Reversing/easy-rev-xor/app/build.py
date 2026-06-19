import os

FLAG = os.environ.get('FLAG') or 'HL4{placeholder_flag_here}'
KEY = 0x1F

encoded = [b ^ KEY for b in FLAG.encode('utf-8')]
arr = ', '.join(f'0x{b:02x}' for b in encoded)

with open('flag_data.h', 'w') as f:
    f.write(f'#define FLAG_LEN {len(FLAG)}\n')
    f.write(f'#define XOR_KEY 0x{KEY:02x}\n')
    f.write(f'static const unsigned char enc[] = {{{arr}}};\n')

print(f'[build] flag_data.h generated — {len(FLAG)} bytes, key=0x{KEY:02x}')
