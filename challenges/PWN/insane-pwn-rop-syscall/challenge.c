#include <stdio.h>
#include <unistd.h>

void vuln(void) {
    char buf[64];
    puts("[*] Input:");
    read(STDIN_FILENO, buf, 256);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("MINIMALIST Corp -- Syscall ROP Interface");
    puts("No shortcuts. Build your chain.");
    vuln();
    return 0;
}
