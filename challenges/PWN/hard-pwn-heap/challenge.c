/*
 * HEAP Corp — Note Manager v0.1
 *
 * Protections: NX=on | PIE=off | Canary=off | RELRO=partial
 *
 * Bug: free() en cmd_del() no pone el puntero a NULL.
 *      El puntero queda "colgando" — dangling pointer.
 *      cmd_edit() escribe desde el INICIO del chunk (sobrescribe fn).
 *
 * Intended path (Use-After-Free + function pointer overwrite):
 *   1. new  slot 0  → malloc(64): Note{fn=display, msg="..."}
 *   2. del  slot 0  → free(slot0) [chunk en tcache]; puntero NO limpiado
 *   3. new  slot 1  → malloc(64): reutiliza el mismo chunk
 *                     (heap[0] y heap[1] apuntan al mismo bloque)
 *   4. edit slot 0  → escribe p64(win) en los primeros 8 bytes del chunk
 *                     (sobrescribe heap[1]->fn también, mismo bloque)
 *   5. read slot 1  → llama heap[1]->fn() == win() → flag
 *
 * La dirección de win() es fija: PIE=off → objdump -d notectl | grep win
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SLOTS 4

typedef struct {
    void (*fn)(void);   /* puntero a función — primeros 8 bytes */
    char  msg[56];      /* mensaje de la nota                   */
} Note;

static Note *heap[SLOTS];

static void display(void) { puts("[NOTE] No hay nada especial aqui."); }

static void win(void) {
    char buf[64];
    FILE *f = fopen("/home/ctf/flag.txt", "r");
    if (!f) { puts("[ERR] flag.txt no encontrado"); return; }
    fgets(buf, sizeof(buf), f);
    fclose(f);
    puts("[SYSTEM] Acceso clasificado concedido.");
    puts(buf);
    _exit(0);
}

static int read_int(void) {
    char tmp[16];
    if (!fgets(tmp, sizeof(tmp), stdin)) return -1;
    return atoi(tmp);
}

static void cmd_new(void) {
    printf("Slot (0-%d): ", SLOTS - 1);
    int s = read_int();
    if (s < 0 || s >= SLOTS) { puts("[ERR] Slot invalido."); return; }
    if (heap[s]) { puts("[ERR] Slot ocupado. Elimina primero."); return; }
    heap[s] = malloc(sizeof(Note));
    heap[s]->fn = display;
    printf("Mensaje: ");
    fgets(heap[s]->msg, sizeof(heap[s]->msg), stdin);
    heap[s]->msg[strcspn(heap[s]->msg, "\n")] = '\0';
    printf("[+] Nota %d creada.\n", s);
}

static void cmd_del(void) {
    printf("Slot (0-%d): ", SLOTS - 1);
    int s = read_int();
    if (s < 0 || s >= SLOTS || !heap[s]) { puts("[ERR] Slot invalido o vacio."); return; }
    free(heap[s]);
    /* BUG: heap[s] NO se pone a NULL — dangling pointer */
    printf("[+] Nota %d eliminada.\n", s);
}

static void cmd_read(void) {
    printf("Slot (0-%d): ", SLOTS - 1);
    int s = read_int();
    if (s < 0 || s >= SLOTS || !heap[s]) { puts("[ERR] Slot invalido o vacio."); return; }
    heap[s]->fn();   /* UAF: puede llamar a un puntero sobrescrito */
}

static void cmd_edit(void) {
    printf("Slot (0-%d): ", SLOTS - 1);
    int s = read_int();
    if (s < 0 || s >= SLOTS || !heap[s]) { puts("[ERR] Slot invalido o vacio."); return; }
    printf("Datos (raw, hasta %zu bytes): ", sizeof(Note));
    /* Escribe desde el INICIO del chunk — permite sobrescribir fn */
    read(STDIN_FILENO, (char *)heap[s], sizeof(Note));
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    puts("=====================================");
    puts("  HEAP Corp -- Note Manager v0.1   ");
    puts("=====================================");
    while (1) {
        puts("\n[1] Nueva  [2] Eliminar  [3] Leer  [4] Editar  [5] Salir");
        printf("> ");
        switch (read_int()) {
            case 1: cmd_new();  break;
            case 2: cmd_del();  break;
            case 3: cmd_read(); break;
            case 4: cmd_edit(); break;
            case 5: return 0;
            default: puts("[ERR] Opcion no valida.");
        }
    }
}
