# Guía Básica de GitHub Codespaces

GitHub Codespaces es un entorno de desarrollo en la nube que te permite programar directamente desde tu navegador o con Visual Studio Code, sin necesidad de instalar herramientas localmente. Es ideal para proyectos colaborativos, pruebas rápidas o cuando necesitas un entorno limpio y reproducible.

---

## ¿Qué es Codespaces?

- Es una “máquina virtual” preconfigurada con soporte para múltiples lenguajes (Python, Node, Go, etc).
- Incluye editor, terminal, depurador y todas las herramientas de desarrollo, en la nube.
- Permite abrir, modificar y probar código de cualquier repo de GitHub en minutos.

---

## ¿Para qué sirve?

- Trabajar en proyectos sin instalar dependencias locales.
- Probar cambios en un entorno limpio y seguro.
- Colaborar más fácil con tu equipo (todos usan el mismo entorno).
- Onboarding rápido para nuevos proyectos.

---

## ¿Cómo se usa?

1. **Desde GitHub:**
   - Entra al repo deseado.
   - Haz clic en el botón verde **“Code”**.
   - Selecciona **“Open with Codespaces”** → **“New codespace”**.
   - Espera unos segundos y tendrás un VSCode completo en tu navegador.

2. **Desde Visual Studio Code (local):**
   - Instala la extensión “GitHub Codespaces”.
   - Conéctate a tu Codespace como si fuera una carpeta remota.

---

## Funcionalidades principales

- **Terminal integrada**: Acceso shell como si fuera tu PC.
- **Customización**: Puedes definir el entorno con archivos `.devcontainer`.
- **Persistencia**: Los cambios se guardan en tu Codespace y puedes hacer commits al repo.
- **Extensiones**: Instala plugins de VSCode como quieras.

---

## Límites y consideraciones

- **Espacio y recursos**: Hay límites de CPU, RAM y disco según tu plan.
- **Duración**: El Codespace se apaga si no lo usás por un tiempo.
- **No recomendado para archivos muy grandes o modelos LLM pesados** (es mejor usar nubes externas para eso).

---

## Ejemplo de uso rápido

```bash
# Una vez en el Codespace:
git clone https://github.com/IOTHernan/CAMBALACHE.git
cd CAMBALACHE
./test.sh
```

---

## ¿Cuánto cuesta?

- Hay un límite gratuito mensual para usuarios individuales.
- Los equipos y organizaciones pueden tener costos según uso.

---

## Más info

- [Documentación oficial](https://docs.github.com/en/codespaces)
- [Guía rápida en español](https://docs.github.com/es/codespaces/getting-started)

---

> **Consejo:** Usá Codespaces para experimentar y colaborar, pero para producción o trabajo intensivo con datos grandes, seguí usando tu entorno local o la nube que prefieras.
