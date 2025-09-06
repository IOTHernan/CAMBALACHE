# CAMBALACHE / Codenames - Comandos Prácticos

## Ejecutar comandos Lisp

```bash
./lispact "(+ 1 2)"
./lispact "(defun saludo () (print \"Hola equipo\"))"
./lispact "(saludo)"
```

## Manejo de VMs

```bash
./cambalache_bin start_vm test_vm
./cambalache_bin stop_vm test_vm
```

## Permisos

```bash
./cambalache_bin grant_permission dev1 VM1
./cambalache_bin revoke_permission dev1 VM1
```

## Probar todo junto

```bash
chmod +x test.sh
./test.sh
```