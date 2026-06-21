#include <stdio.h>
#include <unistd.h>

// No win() function — must build ROP chain

void vuln(void) {
    char buf[64];
    puts("[*] Enter your data:");
    read(STDIN_FILENO, buf, 256);  // overflow: 256 into 64
    puts("[-] Processing complete.");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    puts("=======================================");
    puts("  NetSec Corp -- Data Processing Unit ");
    puts("=======================================");
    vuln();
    return 0;
}
