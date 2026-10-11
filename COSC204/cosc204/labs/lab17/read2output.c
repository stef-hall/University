/* simple-cat.c */
#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/* A common modern disk block size is 4 kiB, and
 * 0x1000 is 4096 in decimal.
 * We don't have to use that, and it's often more efficient
 * to process larger chunks of data at a time.
 */
#define BLOCK_SIZE 0x1000

char buf[BLOCK_SIZE];

int main(int argc, char *argv[]) {

    if (argc < 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    for (int i=1;i<argc;i++) {

        int fd = open(argv[1], O_RDONLY);

        if (fd < 0) {
            perror("open");
            exit(EXIT_FAILURE);
        }

        while (true) {
            ssize_t bytes_read = read(fd, buf, BLOCK_SIZE);

            if (bytes_read < 0) {
                perror("read");
                close(fd);
                exit(EXIT_FAILURE);
            }

            if (bytes_read == 0) { /* end of file */
                break;
            }

            ssize_t bytes_written = 0;

            while (bytes_written < bytes_read) {
                ssize_t res = write(
                    STDOUT_FILENO,
                    buf + bytes_written,
                    bytes_read - bytes_written
                );

                if (res < 0) {
                    perror("write");
                    close(fd);
                    exit(EXIT_FAILURE);
                }

                bytes_written += res;
            }
        }
        close(fd);
    }

    

    return EXIT_SUCCESS;
}