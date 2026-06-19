import os

FLAG = os.environ.get('FLAG') or 'HL4{placeholder_flag_here}'

# Encoding: target[i] = (flag[i] * 31 + i * 7) % 256
# Reverse:  flag[i] = ((target[i] - i*7) * 223) % 256
# (223 is the modular inverse of 31 mod 256: 31 * 223 ≡ 1 mod 256)
target = [(ord(c) * 31 + i * 7) % 256 for i, c in enumerate(FLAG)]
arr = ', '.join(f'0x{b:02x}' for b in target)

with open('flag_data.h', 'w') as f:
    f.write(f'#define FLAG_LEN {len(FLAG)}\n')
    f.write(f'static const unsigned char target[] = {{{arr}}};\n')

print(f'[build] flag_data.h generated — {len(FLAG)} chars encoded')
