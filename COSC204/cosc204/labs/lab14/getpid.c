#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
    pid_t pid = getpid();
    printf("My process ID is %d.\n", pid);
    return EXIT_SUCCESS;
}

/*
strace ./getpid.exe
strace -e inject=getpid:delay_enter=2s ./getpid.exe
strace -e inject=mmap:delay_enter=500ms ./getpid.exe
*/