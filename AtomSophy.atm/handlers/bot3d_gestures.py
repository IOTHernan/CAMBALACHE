import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
import pyttsx3

class Bot3DWindow(QWidget):
    def __init__(self, modelo_path):
        super().__init__()
        self.modelo_path = modelo_path
        self.initUI()
        self.offset = None
        self.gestures = {
            "wave_hand": self.gesture_wave_hand,
            "nod_head": self.gesture_nod_head,
            "shake_head": self.gesture_shake_head,
        }

    def initUI(self):
        self.setWindowTitle('AtomSophy Bot 3D')
        self.resize(400, 250)

        layout = QVBoxLayout()

        self.label = QLabel(f'Model 3D: {self.modelo_path}', self)
        self.label.setStyleSheet("background-color: lightgray; border: 1px solid black; padding: 20px; min-height: 100px;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.combo_gestures = QComboBox(self)
        self.combo_gestures.addItems(list(self.gestures.keys()))
        layout.addWidget(self.combo_gestures)

        self.btn_animar = QPushButton('Perform Gesture', self)
        self.btn_animar.clicked.connect(self.perform_gesture)
        layout.addWidget(self.btn_animar)

        self.setLayout(layout)
        
    # Window drag handlers
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def perform_gesture(self):
        gesture_name = self.combo_gestures.currentText()
        gesture_func = self.gestures.get(gesture_name)
        if gesture_func:
            gesture_func()
        else:
            self.label.setText("Gesture not found.")

    # Gestures implementations (simulated)

    def gesture_wave_hand(self):
        self.label.setText("Gesture: Wave Hand 👋")
        self.modular_voz("Waving hand.", velocidad=130, volumen=0.8)
        # Aquí podés añadir animación real o cambios visuales

    def gesture_nod_head(self):
        self.label.setText("Gesture: Nod Head 🤖")
        self.modular_voz("Nodding head.", velocidad=130, volumen=0.8)

    def gesture_shake_head(self):
        self.label.setText("Gesture: Shake Head 🙅")
        self.modular_voz("Shaking head.", velocidad=130, volumen=0.8)

    def modular_voz(self, texto, velocidad=150, volumen=1.0):
        engine = pyttsx3.init()
        engine.setProperty('rate', velocidad)
        engine.setProperty('volume', volumen)
        engine.say(texto)
        engine.runAndWait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    modelo_path = "data/media/bot_model.gltf"
    ventana = Bot3DWindow(modelo_path)
    ventana.show()
    sys.exit(app.exec_())
