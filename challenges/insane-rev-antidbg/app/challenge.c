/*
 * antidbg — Anti-Debug Crackme
 * AntiDbg Corp v2
 *
 * Protecciones:
 *   1. ptrace self-check: si un debugger esta adjunto, ptrace(PTRACE_TRACEME)
 *      retorna -1 en lugar de 0.
 *   2. timing check: mide cuanto tarda un busy-loop. Si tarda mas de 500ms,
 *      probablemente el proceso esta siendo stepped.
 *
 * La flag esta XOR-encoded con 0x1F en encoded_flag[] (generado por build.py).
 * Para bypassear:
 *   - NOP los saltos condicionales de is_debugged() y timing_check()
 *   - O usar LD_PRELOAD para override ptrace()
 *   - O analisis estatico: extraer encoded_flag[] y XOR con 0x1F
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <time.h>
#include <stdlib.h>

/* Declaraciones externas — definidas en flag_data.c generado por build.py */
extern unsigned char encoded_flag[];
extern int encoded_flag_len;

/* Anti-debug check 1: ptrace self-check
 * Un proceso puede llamar ptrace(PTRACE_TRACEME) una sola vez.
 * Si ya hay un debugger adjunto, la llamada falla y retorna -1.
 */
static int is_debugged(void)
{
    return ptrace(PTRACE_TRACEME, 0, 0, 0) == -1 ? 1 : 0;
}

/* Anti-debug check 2: timing check
 * Mide cuanto tarda un busy-loop de 1M iteraciones.
 * En ejecucion normal: < 10ms.
 * Con breakpoints o single-step: puede pasar 500ms.
 */
static int timing_check(void)
{
    struct timespec t1, t2;
    volatile long x = 0;

    clock_gettime(CLOCK_MONOTONIC, &t1);

    /* Busy-loop: rapido en ejecucion normal */
    for (int i = 0; i < 1000000; i++) {
        x += i;
        x ^= (i & 0xFF);
    }

    clock_gettime(CLOCK_MONOTONIC, &t2);

    long elapsed_ns = (t2.tv_sec  - t1.tv_sec)  * 1000000000L
                    + (t2.tv_nsec - t1.tv_nsec);

    /* Umbral: 500ms = 500,000,000 ns */
    return elapsed_ns > 500000000L ? 1 : 0;
}

/* Decodifica la flag XOR 0x1F y compara con el input */
static void check_flag(const char *input)
{
    char decoded[256];
    int len = encoded_flag_len;

    if (len <= 0 || len > 255) {
        puts("[!] Internal error.");
        return;
    }

    for (int i = 0; i < len; i++) {
        decoded[i] = (char)(encoded_flag[i] ^ 0x1F);
    }
    decoded[len] = '\0';

    if (strcmp(input, decoded) == 0) {
        puts("[+] CORRECT! Access granted.");
    } else {
        puts("[-] Wrong key. Keep trying.");
    }

    /* Limpiar memoria sensible */
    memset(decoded, 0, sizeof(decoded));
}

int main(void)
{
    char input[256];

    /* Deshabilitar buffering para output inmediato */
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    /* ── Check 1: ptrace ── */
    if (is_debugged()) {
        puts("[!] Debugger detected. Access denied.");
        /* Retornar un codigo de salida aleatorio para dificultar analisis */
        return (int)(time(NULL) & 0xFF) | 1;
    }

    /* ── Check 2: timing ── */
    if (timing_check()) {
        puts("[!] Execution anomaly detected. Access denied.");
        return (int)(time(NULL) & 0xFF) | 2;
    }

    /* ── Input ── */
    printf("AntiDbg Corp v2 -- Enter key: ");
    if (fgets(input, (int)sizeof(input), stdin) == NULL) {
        return 1;
    }

    /* Eliminar newline */
    input[strcspn(input, "\n")] = '\0';

    check_flag(input);

    return 0;
}
