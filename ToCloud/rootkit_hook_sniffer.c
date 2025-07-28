/*
 * che_syscall_hook_sniffer.c
 * Sniffer de syscalls hookeadas en entorno de laboratorio.
 * Para sistemas Linux (x86_64). Uso ético y en sandbox.
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

#define MAX_LINE 512
#define TARGET_SYSCALL "getdents64"

void analizar_kallsyms() {
    FILE *fp = fopen("/proc/kallsyms", "r");
    if (!fp) {
        perror("No se pudo abrir /proc/kallsyms");
        exit(EXIT_FAILURE);
    }

    char linea[MAX_LINE];
    while (fgets(linea, MAX_LINE, fp)) {
        if (strstr(linea, TARGET_SYSCALL)) {
            printf("[+] Encontrado: %s", linea);
        }
    }
    fclose(fp);
}

void detectar_syscall_hook() {
    printf("[*] Analizando posibles hooks sobre syscall: %s\n", TARGET_SYSCALL);
    analizar_kallsyms();
}

int main() {
    printf("[Hermes] Módulo de detección de hooks sobre rootkits\n");
    detectar_syscall_hook();
    return 0;
}
