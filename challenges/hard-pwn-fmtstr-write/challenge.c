#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void win(void) {
    char buf[64];
    FILE *f = fopen("/home/ctf/flag.txt", "r");
    if (!f) { puts("flag.txt not found"); return; }
    fgets(buf, sizeof(buf), f);
    fclose(f);
    puts("[+] Acceso concedido:");
    puts(buf);
    _exit(0);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    char log[256];
    puts("LogSys Corp -- Sistema de Registro");
    puts("Introduce el mensaje de log:");
    fgets(log, sizeof(log), stdin);
    log[strcspn(log, "\n")] = '\0';
    printf("[LOG] ");
    printf(log);          /* FORMAT STRING VULNERABILITY */
    puts("\n[*] Sesion cerrada.");
    exit(0);              /* Target: overwrite exit@GOT with win() */
}
