from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QScrollArea,
                            QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt, QTimer
import sys

class FileComparer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comparador de Archivos")
        self.setGeometry(0, 0, 800, 600)
        self.show()

    def load_file1(self):
        file, _ = QFileDialog.getOpenFileName(
            None, "Cargar Archivo 1", "", "Archivos: *.txt; *.docx; *.xls; *.xlsx")
        if file:
            self.file1 = file
            self.load_file(file)

    def load_file2(self):
        file, _ = QFileDialog.getOpenFileName(
            None, "Cargar Archivo 2", "", "Archivos: *.txt; *.docx; *.xls; *.xlsx")
        if file:
            self.file2 = file
            self.load_file(file)

    def load_file(self, file):
        if not file:
            return

        # Determinar si es texto o binario
        if file.lower().endswith('.txt'):
            text = open(file).read()
            self.textEdit.setPlainText(text)
        else:
            bytes_content = open(file, 'rb').read()
            text = bytes_content.decode('utf-8', errors='ignore')
            self.textEdit.setPlainText(text)

    def toggle_zoom(self):
        if hasattr(self.textEdit, 'setZoomAction'):
            if self.is_zoomed():
                self.textEdit.setZoomAction(Qt.NoZoom)
            else:
                self.textEdit.setZoomAction(Qt.External)
        else:
            # Si no Soporte a zoom
            pass

    def is_zoomed(self):
        return hasattr(self.textEdit, 'isZoomed') and \
               getattr(self.textEdit, 'isZoomed', False)

    def show_difference(self):
        if self.file1 and self.file2:
            diff = self.file1 + "\n" + self.file2
            self.textEdit.setPlainText(diff)
            # Implementar la lógica de colorear las diferencias
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileComparer()
    sys.exit(app.exec())