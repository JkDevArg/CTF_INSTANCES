/*
 * Lab03 — Binario vulnerable ARM32 educativo
 * Demuestra shellcode en arquitectura ARM
 */
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void vulnerable_arm(char *input) {
    char buf[48];
    strcpy(buf, input);   // VULNERABILIDAD: sin límite
    printf("ARM32: %s\n", buf);
}

int main() {
    char input[200];
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    printf("=== Lab03 PWN ARM32 ===\n> ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = '\0';
    vulnerable_arm(input);
    return 0;
}
