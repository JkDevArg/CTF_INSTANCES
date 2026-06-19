#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SLOTS 4

void (*action)(void) = NULL;  /* Global function pointer */

typedef struct {
    char data[48];
} Chunk;

Chunk *chunks[SLOTS];

void flag_handler(void) {
    char buf[64];
    FILE *f = fopen("/home/ctf/flag.txt", "r");
    if (!f) { puts("flag not found"); return; }
    fgets(buf, sizeof(buf), f);
    fclose(f);
    puts("[SECRET] Flag:");
    puts(buf);
    _exit(0);
}

void default_action(void) { puts("[INFO] Action triggered."); }

static int read_int(void) {
    char t[8];
    fgets(t, sizeof(t), stdin);
    return atoi(t);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    action = default_action;

    puts("=== AllocatorCorp Note System ===");
    printf("[*] flag_handler @ %p\n", flag_handler);   /* intentional leak */
    printf("[*] action ptr   @ %p\n", &action);         /* intentional leak */

    while (1) {
        puts("[1] Alloc [2] Free [3] Write [4] Show [5] Call [6] Exit");
        printf("> ");
        switch (read_int()) {
            case 1: {
                printf("Slot: ");
                int s = read_int();
                if (s < 0 || s >= SLOTS || chunks[s]) break;
                chunks[s] = malloc(sizeof(Chunk));
                memset(chunks[s], 0, sizeof(Chunk));
                printf("[+] Allocated slot %d\n", s);
                break;
            }
            case 2: {
                printf("Slot: ");
                int s = read_int();
                if (s < 0 || s >= SLOTS || !chunks[s]) break;
                free(chunks[s]);
                /* BUG: pointer not cleared — allows double-free */
                printf("[+] Freed slot %d\n", s);
                break;
            }
            case 3: {
                printf("Slot: ");
                int s = read_int();
                if (s < 0 || s >= SLOTS || !chunks[s]) break;
                printf("Data: ");
                fgets(chunks[s]->data, sizeof(Chunk), stdin);
                break;
            }
            case 4: {
                printf("Slot: ");
                int s = read_int();
                if (s < 0 || s >= SLOTS || !chunks[s]) break;
                printf("[CHUNK %d] %p: ", s, chunks[s]);
                write(STDOUT_FILENO, chunks[s], sizeof(Chunk));
                puts("");
                break;
            }
            case 5:
                action();
                break;
            case 6:
                return 0;
        }
    }
}
