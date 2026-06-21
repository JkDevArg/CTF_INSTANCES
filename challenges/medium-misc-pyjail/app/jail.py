#!/usr/bin/env python3
import sys

ALLOWED_BUILTINS = {
    'print', 'len', 'range', 'str', 'int', 'list', 'dict', 'tuple',
    'type', 'dir', 'vars', 'getattr', 'hasattr', 'repr', 'chr', 'ord',
    'hex', 'bin', 'oct', 'abs', 'bool', 'bytes', 'id', 'isinstance'
}

_real_builtins = __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__)
sandbox_builtins = {k: _real_builtins[k] for k in ALLOWED_BUILTINS if k in _real_builtins}

SANDBOX_GLOBALS = {
    '__builtins__': sandbox_builtins,
    '__name__':     '__restricted__',
}

sys.stdout.write("PyJail v1.0 -- Python Restringido\n")
sys.stdout.write("Builtins disponibles: " + ", ".join(sorted(ALLOWED_BUILTINS)) + "\n")
sys.stdout.write("Flag en: /home/ctf/flag.txt\n\n")
sys.stdout.flush()

while True:
    try:
        sys.stdout.write(">>> ")
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:
            break
        line = line.rstrip('\n')
        if not line:
            continue
        result = eval(line, dict(SANDBOX_GLOBALS))
        if result is not None:
            sys.stdout.write(repr(result) + '\n')
            sys.stdout.flush()
    except SystemExit:
        sys.exit(0)
    except Exception as e:
        sys.stdout.write(f"[!] {type(e).__name__}: {e}\n")
        sys.stdout.flush()
