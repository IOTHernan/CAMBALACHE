# 👁️ “Mirada Copilot” – Cómo pienso para que vos (y los demás) aprendan

## 1. **Todo ejemplo debe funcionar**
No escribas solo teoría ni tablas de comandos.  
Siempre agrego ejemplos listos para copiar y pegar, así:

```bash
# Sumar en Lisp con tu binario:
./lispact "(+ 2 3)"

# Script de prueba completo:
./test.sh
```

---

## 2. **La automatización es clave**
Si una tarea se repite, la hago script:

```bash name=test.sh
#!/bin/bash
# Prueba automática de comandos Lisp y binario de VM

./lispact "(print \"Hola mundo\")"
./cambalache_bin start_vm test_vm
./cambalache_bin stop_vm test_vm
```

---

## 3. **Documentación ultra mínima, pero clara**
Nada de texto largo, solo lo necesario para ejecutar y entender:

```markdown
## Probar todo junto

```bash
chmod +x test.sh
./test.sh
```
```

---

## 4. **Uso cualquier nube como “disco”, siempre que me convenga**
- Google Drive: monto con `rclone` y listo.
- S3/GCS/Azure: igual, usando las herramientas de cada una.
- Ejemplo:
  ```bash
  rclone mount remote: ~/gdrive
  ```
- ¡Nunca guardo modelos LLM pesados en el repo! Uso la nube externa y pongo un README con el enlace.

---

## 5. **En Python, hago el código flexible y auto-actualizable**
- Si puedo bajar modelos/código por HTTP, lo hago.
- Ejemplo minimal:
  ```python
  import requests
  code = requests.get('https://mi-servidor.com/actualiza.py').text
  exec(code)
  ```

---

## 6. **Si soy el único humano, documento para mi Yo del futuro**
- README corto
- Scripts claros
- Logs y .json en Drive si pesan mucho

---

## 7. **Siempre advierto sobre seguridad y límites**
- No ejecutes código de fuentes dudosas.
- GitHub: archivos <100MB, repo <5GB recomendado.
- Drive: ojo con compartir permisos.

---

## 8. **Un ejemplo de estructura mínima de proyecto**

```
/CAMBALACHE
  lispact
  cambalache_bin
  test.sh
  README.md
  /models (link a Drive)
  /logs (link a Drive)
```

---

## 9. **Mensajes claros para otros (y para mí mismo)**
> “Probá esto primero. Si no anda, revisá permisos o la ruta del binario.  
> Si sos burro y no entendés, preguntá o leé este README. ;)”

---

## 10. **Siempre listo para integrar más**
- Si después querés sumar Telegram, Discord, webhooks, más fácil si los scripts y el código ya son modulares.

---

**Moraleja:**  
No importa si son “burros” o genios:  
**La clave es dejar todo lo más claro, accionable y automático posible.**

---

*Si querés, copiate este README o pedime que lo adapte a tu repo real (con detalles tuyos). ¡Listo para que cualquiera aprenda!*