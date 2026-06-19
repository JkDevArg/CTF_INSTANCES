#include <stdio.h>
#include <unistd.h>

void win(void) {
    char buf[64];
    FILE *f = fopen("/home/ctf/flag.txt", "r");
    if (!f) { puts("flag.txt not found"); return; }
    fgets(buf, sizeof(buf), f);
    fclose(f);
    puts("[+] SAFE OPENED:");
    puts(buf);
    _exit(0);
}

void vuln(void) {
    char input[40];
    write(STDOUT_FILENO, "Access code: ", 13);
    /* 42 bytes: fills input[40] + 2 bytes of saved rbp = partial overwrite of ret addr */
    read(STDIN_FILENO, input, 42);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    puts("SafeBox Corp -- Secure Vault v3");
    vuln();
    return 0;
}
