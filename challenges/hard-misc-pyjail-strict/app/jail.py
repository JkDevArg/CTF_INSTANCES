#!/usr/bin/env python3
import sys

# Completely empty builtins — not even print
SANDBOX = {'__builtins__': {}, '__name__': 'jail'}

sys.stdout.write("PyJail v2.0 -- Maxima Seguridad\n")
sys.stdout.write("__builtins__ = {}\n")
sys.stdout.write("Buenas suerte.\n\n")
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
        result = eval(line, dict(SANDBOX))
        if result is not None:
            sys.stdout.write(str(result) + '\n')
            sys.stdout.flush()
    except SystemExit:
        sys.exit(0)
    except Exception as e:
        sys.stdout.write(f"[!] {type(e).__name__}: {e}\n")
        sys.stdout.flush()
