#!/bin/bash

echo "== Prueba de Lispact =="
./lispact "(+ 1 2)"
./lispact "(defun saludo () (print \"Hola equipo\"))"
./lispact "(saludo)"

echo "== Prueba de manejo de VM =="
./cambalache_bin start_vm test_vm
./cambalache_bin stop_vm test_vm

echo "== Prueba de permisos =="
./cambalache_bin grant_permission dev1 VM1
./cambalache_bin revoke_permission dev1 VM1