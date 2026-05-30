/*
 * Lab03 — Crackme educativo para reversing
 * Objetivo: encontrar la contraseña correcta analizando el binario
 * Técnicas: strings, ltrace, strace, Ghidra, GDB
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Contraseña ofuscada (XOR con 0x42) — ¡debes recuperarla!
static const unsigned char enc_pass[] = {
    0x23, 0x27, 0x30, 0x26, 0x2f, 0x2c, 0x62, 0x31, 0x34, 0x27, 0x62,
    0x39, 0x34, 0x22, 0x60, 0x37, 0x22, 0x38, 0x00
};  // XOR 0x42 de "admin_true_xor_pass"

void decode(const unsigned char *in, char *out, int len) {
    for (int i = 0; i < len; i++) out[i] = in[i] ^ 0x42;
    out[len] = '\0';
}

int check_password(const char *input) {
    char expected[64];
    decode(enc_pass, expected, sizeof(enc_pass) - 1);
    return strcmp(input, expected) == 0;
}

int main() {
    char attempt[128];
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);

    printf("=== Lab03 Crackme — Reversing Challenge ===\n");
    printf("Ingresa la contraseña: ");
    fgets(attempt, sizeof(attempt), stdin);
    attempt[strcspn(attempt, "\n")] = '\0';

    if (check_password(attempt)) {
        printf("✅ ¡Correcto!\nFLAG{r3v3rs1ng_xor_0bf4sc4t10n}\n");
    } else {
        printf("❌ Incorrecto. Pista: analiza la función decode() con Ghidra.\n");
    }
    return 0;
}
