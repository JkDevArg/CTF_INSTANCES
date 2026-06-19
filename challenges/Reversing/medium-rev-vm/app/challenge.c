#include <stdio.h>
#include <string.h>
#include "bytecode.h"

#define OP_CHECK  0x01
#define OP_HALT   0x02
#define OP_FAIL   0x03

static void run(const char *input) {
    size_t inlen = strlen(input);
    int ip = 0;

    while (ip < PROG_LEN) {
        unsigned char op = prog[ip++];

        if (op == OP_CHECK) {
            unsigned char idx      = prog[ip++];
            unsigned char expected = prog[ip++];
            if (idx >= inlen) {
                puts("Wrong.");
                return;
            }
            unsigned char got = ((unsigned char)input[idx] ^ (idx * 0x13 + 0x5A)) & 0xFF;
            if (got != expected) {
                puts("Wrong.");
                return;
            }
        } else if (op == OP_HALT) {
            puts("Correct! That's the flag.");
            return;
        } else {
            puts("Wrong.");
            return;
        }
    }
    puts("Wrong.");
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <flag>\n", argv[0]);
        return 1;
    }
    if ((int)strlen(argv[1]) != INPUT_LEN) {
        puts("Wrong.");
        return 1;
    }
    run(argv[1]);
    return 0;
}
