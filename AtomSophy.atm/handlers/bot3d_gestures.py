import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox
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
        self.setGeometry(100, 100, 400, 350)
        
        self.label = QLabel(f'Model 3D: {self.modelo_path}', self)
        self.label.setGeometry(50, 50, 300, 100)
        self.label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.label.setAlignment(Qt.AlignCenter)

        self.combo_gestures = QComboBox(self)
        self.combo_gestures.setGeometry(50, 170, 300, 30)
        self.combo_gestures.addItems(list(self.gestures.keys()))

        self.btn_animar = QPushButton('Perform Gesture', self)
        self.btn_animar.setGeometry(150, 220, 100, 40)
        self.btn_animar.clicked.connect(self.perform_gesture)

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
