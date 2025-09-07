#!/bin/bash
# setup_alian_jr_firmado.sh
# Proyecto Alian_Jr “firmado”, listo para analizar LLM

PROJECT="Alian_Jr"
mkdir -p $PROJECT/data

# personality_array.py
cat > $PROJECT/personality_array.py <<EOL
import numpy as np
import os

class PersonalityArray:
    def __init__(self, rows=2, cols=100, path="data/personality.npy", log_path="data/log.txt"):
        self.path = path
        self.log_path = log_path
        if os.path.exists(path):
            self.array = np.load(path)
        else:
            self.array = np.zeros((rows, cols))
    
    def update(self, index, value, action="update"):
        self.array[:, index] += value
        self._clip()
        self.save()
        self.log_action(action, index, value)
    
    def penalize(self, index, severity=1):
        self.array[:, index] -= severity
        self._clip()
        self.save()
        self.log_action("penalize", index, severity)
    
    def _clip(self):
        self.array = np.clip(self.array, -100, 100)
    
    def save(self):
        np.save(self.path, self.array)
    
    def log_action(self, action, index, value):
        with open(self.log_path, "a") as f:
            f.write(f"{action} en índice {index} -> {value}\n")
EOL

# handlers.py
cat > $PROJECT/handlers.py <<EOL
from personality_array import PersonalityArray
persona = PersonalityArray()

def handle_command(command):
    if "good" in command:
        persona.update(0, 5, action=command)
    elif "bad" in command:
        persona.penalize(0, 3)
    print("Estado actual:", persona.array[:, 0])
EOL

# main.py
cat > $PROJECT/main.py <<EOL
from handlers import handle_command

print("Alian_Jr firmado y listo para competir 🚀")
while True:
    cmd = input(">> ")
    if cmd.lower() in ["exit", "quit"]:
        break
    handle_command(cmd)
EOL

echo "Proyecto $PROJECT firmado y listo para usar."
