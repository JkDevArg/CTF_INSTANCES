/*
 * VAULT Corp — Access Terminal
 *
 * Protections: NX=on | PIE=off | Canary=off | RELRO=partial
 *
 * Bug: read() into a 64-byte stack buffer with a 128-byte limit.
 * There IS a win() function. Find it, point RIP at it.
 *
 * Intended path:
 *   1. Find offset to RIP: 64 (buffer) + 8 (saved rbp) = 72 bytes.
 *   2. Find win() address: objdump -d vault | grep win
 *   3. Overwrite RIP with win() address.
 *   4. win() opens and prints flag.txt.
 */

#include <stdio.h>
#include <unistd.h>

void win(void) {
    char buf[64];
    FILE *f = fopen("/home/ctf/flag.txt", "r");
    if (!f) { puts("[!] flag.txt not found"); return; }
    fgets(buf, sizeof(buf), f);
    fclose(f);
    puts("[+] ACCESS GRANTED");
    puts(buf);
    _exit(0);
}

static void vuln(void) {
    char code[64];
    write(STDOUT_FILENO, "[AUTH] Enter access code: ", 26);
    read(STDIN_FILENO, code, 128);   /* overflow: 128 into 64 */
    puts("[-] Invalid code. Access denied.");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    puts("=========================================");
    puts("  VAULT Corp -- Secure Access Terminal  ");
    puts("=========================================");
    vuln();
    return 0;
}
