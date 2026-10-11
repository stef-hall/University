/* simple-cat.c */
#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define BLOCK_SIZE 0x1000

char buf[BLOCK_SIZE];

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int fd = open(argv[1], O_CREAT);

    if (fd < 0) {
        perror("open");
        exit(EXIT_FAILURE);
    }

    close(fd);

    return EXIT_SUCCESS;
}
