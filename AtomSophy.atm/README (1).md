# CAMBALACHE - Comandos Rápidos

## 🧠 Ejecutar Comandos Lisp

```bash
./lispact "(+ 1 2)"
./lispact "(defun saludo () (print \"Hola equipo\"))"
./lispact "(saludo)"
```

## ⚙️ Comandos Binarios Especiales

### Manejo de VM

```bash
./cambalache_bin start_vm nombre_vm
./cambalache_bin stop_vm nombre_vm
./cambalache_bin restart_vm nombre_vm
```

### Permisos

```bash
./cambalache_bin grant_permission usuario recurso
./cambalache_bin revoke_permission usuario recurso
```

## 🧪 Ejemplo de script de prueba

```bash name=test.sh
#!/bin/bash

# Prueba comandos Lisp
./lispact "(+ 5 7)"
./lispact "(print \"Hola desde script\")"

# Prueba manejo de VM
./cambalache_bin start_vm test_vm
./cambalache_bin stop_vm test_vm

# Prueba permisos
./cambalache_bin grant_permission dev1 VM1
./cambalache_bin revoke_permission dev1 VM1
```

## 🚀 Primeros pasos rápidos

1. Da permisos de ejecución:
   ```bash
   chmod +x lispact cambalache_bin test.sh
   ```
2. Corre el test:
   ```bash
   ./test.sh
   ```

---

**¿Más detalles?**  
Si necesitás agregar nuevos comandos, hacelo en este README y en `test.sh` para que todos puedan probarlos fácil. Nada de rituales, ¡acción concreta!