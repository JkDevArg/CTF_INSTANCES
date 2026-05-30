/*
 * Lab03 — Binario vulnerable educativo x64
 * Demuestra: Stack Buffer Overflow + ROP chains
 * Solo para uso en laboratorio aislado.
 *
 * Compilar: gcc -o vuln vuln.c -fno-stack-protector -no-pie -z execstack -m64
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Función auxiliar — nunca llamada directamente (ROP gadget)
void win_function() {
    char flag[64];
    FILE *f = fopen("/pwn/flag.txt", "r");
    if (f) {
        fgets(flag, sizeof(flag), f);
        fclose(f);
        printf("🎉 ¡Flag encontrada!\n%s\n", flag);
    }
    exit(0);
}

void vulnerable_function(char *input) {
    char buffer[64];            // buffer fijo de 64 bytes
    printf("Procesando: ");
    strcpy(buffer, input);      // VULNERABILIDAD: sin verificación de tamaño
    printf("%s\n", buffer);
}

int main() {
    char input[256];
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);

    printf("=== Lab03 PWN Challenge — x64 ===\n");
    printf("Ingresa tu mensaje:\n> ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = '\0';

    vulnerable_function(input);

    printf("Fin del programa.\n");
    return 0;
}
