import os
import py_compile

FLAG = os.environ.get('FLAG') or 'CTF{placeholder_flag_here}'

# Encode: expected[i] = ord(flag[i]) + i
# Reverse: flag[i] = chr(expected[i] - i)
expected = [ord(c) + i for i, c in enumerate(FLAG)]

src = f'''import sys


def verify(inp):
    expected = {expected}
    if len(inp) != {len(FLAG)}:
        return False
    return [ord(c) + i for i, c in enumerate(inp)] == expected


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python challenge.pyc <flag>")
        sys.exit(1)
    if verify(sys.argv[1]):
        print("Correct!")
    else:
        print("Wrong flag.")
'''

with open('challenge_src.py', 'w') as f:
    f.write(src)

py_compile.compile('challenge_src.py', 'dist/challenge.pyc', doraise=True)
print(f'[build] challenge.pyc compiled ({len(FLAG)} chars)')
