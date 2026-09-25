#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
    pid_t pid = fork();

    if (pid > 0) {
        printf("This is the parent process (pid: %d). ", getpid());
        printf("My child's process ID is %d\n", pid);

    } else if (pid == 0) {
        printf("This is da child process (pid: %d)\n", getpid());

    } else {
        perror("Fork failed bruh");
        exit(EXIT_FAILURE);
    }

    while (1) {}

    return EXIT_SUCCESS;
}