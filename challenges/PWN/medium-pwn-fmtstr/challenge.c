/*
 * ECHO Corp — Logging Service v2
 *
 * Protections: NX=on | PIE=off | Canary=off | RELRO=partial
 *
 * Bug: printf(name) sin especificador de formato.
 * La variable global 'flag' se carga al arrancar y su dirección
 * es fija porque PIE está deshabilitado.
 *
 * Intended path:
 *   1. Encontrar la dirección de 'flag': readelf -s echo | grep flag
 *   2. Construir un payload que coloque esa dirección en la pila.
 *   3. Usar %N$s para desreferenciar el puntero y leer el string.
 *      (El propio buffer 'name' es el primer argumento de la pila
 *       para printf en x86-64 — buscar el offset con %p repetidos.)
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>

char flag[64];

static void init(void) {
    FILE *f = fopen("/home/ctf/flag.txt", "r");
    if (f) {
        fgets(flag, sizeof(flag), f);
        fclose(f);
        flag[strcspn(flag, "\n")] = '\0';
    }
}

static void vuln(void) {
    char name[128];
    write(STDOUT_FILENO, "[ECHO] Introduce tu nombre de usuario: ", 39);
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = '\0';

    printf("Bienvenido, ");
    printf(name);           /* FORMAT STRING VULNERABILITY */
    puts("!");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    init();
    puts("=========================================");
    puts("  ECHO Corp -- Logging Service v2.1    ");
    puts("=========================================");
    vuln();
    return 0;
}
