#include <stdio.h>
#include <string.h>
#include "flag_data.h"

static int check(const char *s) {
    if ((int)strlen(s) != FLAG_LEN) return 0;
    for (int i = 0; i < FLAG_LEN; i++) {
        unsigned char c = (unsigned char)s[i];
        if ((c * 31 + i * 7) % 256 != target[i]) return 0;
    }
    return 1;
}

int main(void) {
    char buf[512];
    printf("Enter the flag: ");
    fflush(stdout);
    if (!fgets(buf, sizeof(buf), stdin)) return 1;
    int len = (int)strlen(buf);
    if (len > 0 && buf[len - 1] == '\n') buf[len - 1] = '\0';
    if (check(buf)) {
        puts("Correct! That's the flag.");
    } else {
        puts("Nope. Keep trying.");
    }
    return 0;
}
