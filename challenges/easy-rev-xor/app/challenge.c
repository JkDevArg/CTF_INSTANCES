#include <stdio.h>
#include <string.h>
#include "flag_data.h"

static void decode(unsigned char *out) {
    for (int i = 0; i < FLAG_LEN; i++) {
        out[i] = enc[i] ^ XOR_KEY;
    }
    out[FLAG_LEN] = '\0';
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <flag>\n", argv[0]);
        return 1;
    }
    unsigned char decoded[256];
    decode(decoded);
    if (strcmp(argv[1], (char *)decoded) == 0) {
        printf("Correct! %s\n", (char *)decoded);
        return 0;
    }
    puts("Wrong flag.");
    return 1;
}
