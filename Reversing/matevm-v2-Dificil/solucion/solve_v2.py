#!/usr/bin/env python3
"""matevm2 author solver.

Recovers the flag from a reconstructed constraint model. In a real solve,
the player would:
  1. Triage the binary, identify the VM and its ISA.
  2. Emulate / instrument the VM (Unicorn, GDB script, or a hand-rolled
     re-implementation in Python) to extract the trace of (op, idxs, target)
     tuples and the rolling-state semantics.
  3. Feed those into Z3.

For the author, the challenge.json produced by gen_challenge.py already
carries the constraint model — this script just reads it and solves.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
CHARSET_BYTES = [ord(c) for c in CHARSET]


def solve(model: dict) -> str | None:
    from z3 import (
        BitVec, BitVecVal, Solver, Or, sat, RotateLeft, Extract, ZeroExt,
    )

    n = model["body_len"]
    body = [BitVec(f"b{i}", 8) for i in range(n)]
    s = Solver()

    for v in body:
        s.add(Or(*[v == BitVecVal(c, 8) for c in CHARSET_BYTES]))

    def byte_of(state32, lo):
        return Extract(lo * 8 + 7, lo * 8, state32)

    def rl8(v, k):
        k &= 7
        return RotateLeft(v, k) if k else v

    def rl32(v, k):
        k &= 31
        return RotateLeft(v, k) if k else v

    def sym_eval(op, args, state32):
        s0 = byte_of(state32, 0)
        if op == "xor2":
            a, b = args
            return a ^ b ^ s0
        if op == "win2":
            a, b = args
            return a * BitVecVal(37, 8) + b * BitVecVal(211, 8) + s0
        if op == "sum3":
            a, b, c = args
            return (a + b + c) ^ byte_of(state32, 1)
        if op == "mix3":
            a, b, c = args
            return rl8(a, 3) ^ rl8(b, 5) ^ c ^ byte_of(state32, 2)
        if op == "tri":
            a, b, c = args
            return (
                a
                ^ rl8(b, 4)
                ^ (c * BitVecVal(5, 8) + BitVecVal(11, 8))
                ^ byte_of(state32, 3)
            )
        raise ValueError(op)

    def sym_update(state32, args, value8):
        for v in args:
            state32 = rl32(state32 ^ ZeroExt(24, v), 7)
            state32 = state32 + (ZeroExt(24, v) << BitVecVal(16, 32))
        state32 = (
            rl32(state32, 13)
            ^ (ZeroExt(24, value8) << BitVecVal(8, 32))
            ^ BitVecVal(0x9E3779B9, 32)
        )
        return state32

    state = BitVecVal(model["initial_state"], 32)
    for c in model["constraints"]:
        args_vars = [body[i] for i in c["idxs"]]
        target_const = BitVecVal(c["target"], 8)
        s.add(sym_eval(c["op"], args_vars, state) == target_const)
        state = sym_update(state, args_vars, target_const)

    crc = BitVecVal(0xCAFEBABE, 32)
    for v in body:
        crc = rl32(crc, 5) ^ ZeroExt(24, v)
        crc = crc + BitVecVal(0x9E3779B9, 32)
        crc = rl32(crc, 11) ^ (ZeroExt(24, v) << BitVecVal(17, 32))
    s.add(crc == BitVecVal(model["checksum_target"], 32))

    if s.check() != sat:
        return None
    m = s.model()
    return "".join(chr(m[v].as_long()) for v in body)


def main() -> None:
    ap = argparse.ArgumentParser()
    default_in = Path(__file__).resolve().parent / "challenge.json"
    ap.add_argument("--input", default=str(default_in),
                    help="path to challenge.json produced by gen_challenge.py")
    args = ap.parse_args()

    with open(args.input) as f:
        ch = json.load(f)

    model = ch["constraints_model"]
    env = ch["envelope"]
    print(f"loaded {args.input}")
    print(f"  body_len     = {model['body_len']}")
    print(f"  constraints  = {len(model['constraints'])}")
    print(f"  checksum     = 0x{model['checksum_target']:08X}")
    print()

    t0 = time.monotonic()
    body = solve(model)
    dt = time.monotonic() - t0
    if body is None:
        print(f"UNSAT  ({dt:.2f}s)")
        sys.exit(1)
    flag = env["prefix"] + body + env["suffix"]
    print(f"flag: {flag}")
    print(f"solved in {dt:.2f}s")


if __name__ == "__main__":
    main()
