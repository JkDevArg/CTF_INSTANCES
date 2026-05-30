/*
 * NEXUS Corp — Secure Authentication Terminal v2.1
 *
 * Protections: NX=on | PIE=on | Canary=on | RELRO=partial
 *
 * Two bugs in this binary:
 *
 * Bug 1 — employee_lookup(): printf(name) without format specifier.
 *   Use it to leak the stack canary and a libc address.
 *   The canary is at a fixed offset in the format string dump.
 *   A libc return address (__libc_start_call_main) is also visible.
 *
 * Bug 2 — authenticate(): read() into a 48-byte buffer with 128-byte limit.
 *   Stack frame:  [password 48B][canary 8B][saved rbp 8B][rip 8B]
 *   With the leaked canary you can overwrite rip cleanly.
 *
 * Intended path:
 *   1. employee_lookup: send "%p."*30 — find canary (ends \x00) + libc ptr.
 *   2. Calculate libc base, system(), /bin/sh.
 *   3. authenticate: A*48 + canary + A*8 + pop_rdi + /bin/sh + ret + system.
 *   4. Shell → cat flag.txt
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>

static void banner(void) {
    puts("================================================");
    puts("  NEXUS Corp -- Secure Authentication Terminal ");
    puts("          >> Version 2.1 PATCHED <<            ");
    puts("  [!] Stack canary & PIE protections active    ");
    puts("================================================");
    puts("");
}

/* Bug 1: format string — use this to leak canary + libc address */
static void employee_lookup(void) {
    char name[64];
    write(STDOUT_FILENO, "[LOOKUP] Employee name: ", 24);
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = '\0';
    printf("[INFO] Searching records for: ");
    printf(name);                          /* format string vulnerability */
    puts("\n[-] Employee not found.\n");
    fflush(stdout);
}

/* Bug 2: stack overflow — use leaked canary here to bypass protection */
static void authenticate(void) {
    char password[48];
    write(STDOUT_FILENO, "[AUTH] Master password: ", 24);
    read(STDIN_FILENO, password, 128);     /* overflow: 128 into 48 */
    puts("[-] Authentication failed.");
    fflush(stdout);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    banner();
    employee_lookup();
    authenticate();
    return 0;
}
