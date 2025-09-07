@echo off
:: setup_alian_jr_firmado.bat
:: Proyecto Alian_Jr “firmado” Windows

set PROJECT=Alian_Jr
mkdir %PROJECT%
mkdir %PROJECT%\data

:: personality_array.py
(
echo import numpy as np
echo import os
echo.
echo class PersonalityArray:
echo.    def __init__(self, rows=2, cols=100, path="data/personality.npy", log_path="data/log.txt"):
echo.        self.path = path
echo.        self.log_path = log_path
echo.        if os.path.exists(path):
echo.            self.array = np.load(path)
echo.        else:
echo.            self.array = np.zeros((rows, cols))
echo.
echo.    def update(self, index, value, action="update"):
echo.        self.array[:, index] += value
echo.        self._clip()
echo.        self.save()
echo.        self.log_action(action, index, value)
echo.
echo.    def penalize(self, index, severity=1):
echo.        self.array[:, index] -= severity
echo.        self._clip()
echo.        self.save()
echo.        self.log_action("penalize", index, severity)
echo.
echo.    def _clip(self):
echo.        self.array = np.clip(self.array, -100, 100)
echo.
echo.    def save(self):
echo.        np.save(self.path, self.array)
echo.
echo.    def log_action(self, action, index, value):
echo.        with open(self.log_path, "a") as f:
echo.            f.write(f"{action} en índice {index} -> {value}\n")
) > %PROJECT%\personality_array.py

:: handlers.py
(
echo from personality_array import PersonalityArray
echo persona = PersonalityArray()
echo.
echo def handle_command(command):
echo.    if "good" in command:
echo.        persona.update(0, 5, action=command)
echo.    elif "bad" in command:
echo.        persona.penalize(0, 3)
echo.    print("Estado actual:", persona.array[:, 0])
) > %PROJECT%\handlers.py

:: main.py
(
echo from handlers import handle_command
echo print("Alian_Jr firmado y listo para competir 🚀")
echo while True:
echo.    cmd = input(">> ")
echo.    if cmd.lower() in ["exit", "quit"]:
echo.        break
echo.    handle_command(cmd)
) > %PROJECT%\main.py

echo Proyecto %PROJECT% firmado y listo para usar.
pause
