# Estructura completa de package extendido: che_getfile

# ===========================
# che_getfile/__init__.py
# ===========================
from .che_getfile import getfile, getfolder, savefile

__all__ = ["getfile", "getfolder", "savefile"]


# ===========================
# che_getfile/che_getfile.py
# ===========================
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

def getfile(text="Selecciona archivo", ext="Todos los archivos (*)", path=".", multi=False):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    if multi:
        files, _ = QFileDialog.getOpenFileNames(None, text, path, ext, options=options)
        return files if files else []
    else:
        file, _ = QFileDialog.getOpenFileName(None, text, path, ext, options=options)
        return file if file else None

def getfolder(text="Selecciona carpeta", path="."):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    folder = QFileDialog.getExistingDirectory(None, text, path)
    return folder if folder else None

def savefile(text="Guardar como", ext="Todos los archivos (*)", path="."):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    file, _ = QFileDialog.getSaveFileName(None, text, path, ext)
    return file if file else None


# ===========================
# setup.py
# ===========================
from setuptools import setup, find_packages

setup(
    name="che_getfile",
    version="1.0.0",
    description="Selector de archivos tipo FoxPro extendido con PyQt5",
    author="Comandante",
    packages=find_packages(),
    install_requires=["PyQt5"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


# ===========================
# README.md
# ===========================
# che_getfile

Selector de archivos al estilo FoxPro extendido con PyQt5. Permite:

- Selección de uno o varios archivos
- Selección de carpetas
- Diálogos de guardado

## Uso

```python
from che_getfile import getfile, getfolder, savefile

archivo = getfile("Seleccionar código", "Python (*.py);;Texto (*.txt)", path="./Hermes/", multi=True)
carpeta = getfolder("Destino de trabajo")
guardar = savefile("Guardar informe", "Texto (*.txt)", path="./logs/")
```

## Instalación

```bash
pip install .
```


# ===========================
# build_package.sh
# ===========================
#!/bin/bash
# Script de construcción del package en venv310

source ~/venv310/bin/activate
rm -rf dist build *.egg-info
python3 setup.py sdist bdist_wheel
echo "📦 Package construido en ./dist"


# ===========================
# Árbol de carpetas sugerido
# ===========================
#
# AtomSophy/
# ├── Hermes/
# │   └── gui/
# │       └── che_getfile/         <-- aquí va el package
# │           ├── __init__.py
# │           └── che_getfile.py
# ├── setup.py                     <-- para che_getfile
# ├── build_package.sh            <-- script de construcción
# └── README.md
