/*
 * NEXUS Corp — Secure Authentication Terminal v1.0
 *
 * Protections: NX=on | PIE=off | Canary=off | RELRO=partial
 *
 * Bug: read() into a 80-byte stack buffer with a 256-byte limit.
 * There is no win() function. Build your own ROP chain.
 *
 * Intended path:
 *   1. Find offset to RIP (80 + 8 = 88 bytes).
 *   2. Leak libc base: ROP → puts(puts@GOT) → ret2main.
 *   3. Calculate system() and /bin/sh from leaked base.
 *   4. ROP → system("/bin/sh") → shell → cat flag.txt
 */

#include <stdio.h>
#include <unistd.h>

static void banner(void) {
    puts("================================================");
    puts("  NEXUS Corp -- Secure Authentication Terminal ");
    puts("           >> Version 1.0 STABLE <<            ");
    puts("================================================");
    puts("");
}

static void authenticate(void) {
    char credentials[80];
    write(STDOUT_FILENO, "[AUTH] Employee credentials: ", 29);
    read(STDIN_FILENO, credentials, 256);   /* overflow: 256 into 80 */
    puts("[-] Authentication failed. Access denied.");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    banner();
    authenticate();
    return 0;
}
