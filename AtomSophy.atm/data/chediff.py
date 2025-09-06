from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QScrollArea,
                            QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt, QTimer
import sys

class FileComparer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        #self.setWindowFlag(Qt.WindowTitle中含有FileIconstu icon, windowTitle="Archivo 1")
        self.setWindowTitle("Comparador de Archivos")
        self.setGeometry(0, 0, 800, 600)
        self.show()

    def init_ui(self):
    	# Crear widgets principales
    	self.text = QTextEdit()
    	other_text = QTextEdit()

    	button_view_diff = QPushButton("Ver Diferencias")
    	button_view_diff.clicked.connect(self.show_difference)

    	menu = self.create_menu()

    	# Agregar menú al widget principal (p.ej., al texto)
    	self.text.setContextMenu(menu)

        # Variables para los archivos
        self.file1 = None
        self.file2 = None

        # Controles
        self.load_button1 = QPushButton("Abrir Archivo 1")
        self.load_button1.clicked.connect(self.load_file1)
        self.load_button2 = QPushButton("Abrir Archivo 2")
        self.load_button2.clicked.connect(self.load_file2)

        # Menú
        #self.create_menu()

        # Área principal
        self.create =selfcomparison_area
        selfcomparison_area = QTextEdit()
        selfcomparison_area.setLineWrapMode(QTextEdit.NoWrap)
        selfcomparison_area.setTabStopInterval(4)

        # Scroll areas y zoom
        self.scroll1 = QScrollArea()
        self.scroll2 = QScrollArea()

        # Botones de control
        self.toggle_zoom_button = QPushButton("ZOOM")
        self.toggle_zoom_button.clicked.connect(self.toggle_zoom)

        # Diseño del layout
        self.create_layout()

    def create_menu(self):
        menu = self.menuBar()
        # Menu "Ayuda"
        submenu.addActions([self.on_help])
        file_action = menu.addAction("Nuevo")
        file_action.triggered.connect(self.clear_files)
        menu.addSubmenu(submenu)
        return menu

    def on_help(self):
        QMessageBox.information(self, "Ayuda", "Sobre este programa")

    def create_layout(self):
        main_layout = QVBoxLayout()

        # Botones de carga
        QHBoxLayout(self, "Cargar Archivo 1", self.load_button1)
        QHBoxLayout(self, "Cargar Archivo 2", self.load_button2)

        # Comparación area
        main_layout.addWidget(selfcomparison_area)

        # Scroll areas
        main_layout.addWidget(self.scroll1)
        main_layout.addWidget(self.scroll2)

        # Botones de control
        main_layout.addWidget(self.toggle_zoom_button)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def load_file1(self):
        file, _ = QFileDialog.getOpenFileName(
            None, "Cargar Archivo 1", "", "Archivos: *.txt; *.docx; *.xls; *.xlsx")
        if file:
        	f1 = self.text.setPlainText(file)
            self.file1 = file
            self.load_file(file)

    def load_file2(self):
        file, _ = QFileDialog.getOpenFileName(
            None, "Cargar Archivo 2", "", "Archivos: *.txt; *.docx; *.xls; *.xlsx")
        if file:
        	other_text.setPlainText(file)
            self.file2 = file
            self.load_file(file)

    def load_file(self, file):
        if not file:
            return

        # Determinar si es texto o binario
        if file.lower().endswith('.txt'):
            text = open(file).read()
            selfcomparison_area.setPlainText(text)

        else:
            bytes_content = open(file, 'rb').read()
            text = bytes_content.decode('utf-8', errors='ignore')
            selfcomparison_area.setPlainText(text)

    def toggle_zoom(self):
        if self.is_zoomed():
            selfcomparison_area.setWindowStyle(
                Qt.WindowType==None,
                Qt.ZoomAction.NoZoom
            )
        else:
            selfcomparison_area.setWindowStyle(
                Qt.WindowType==None,
                Qt.ZoomAction.External
            )

    def is_zoomed(self):
        return hasattr(selfcomparison_area, 'is(ZoomAction)') and \
               getattr(selfcomparison_area, 'is(ZoomAction)', False)

    def show_difference(self):
    	# difference.show()
        pass  # Implementar la lógica de colorear las diferencias

    def clear_files(self):
        self.file1 = None
        self.file2 = None
        selfcomparison_area.clear()
        selfcomparison_area.setLineWrapMode(QTextEdit.NoWrap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileComparer()
    sys.exit(app.exec()) 
#    window = MainWindow()
    window.show()
    sys.exit(app.exec())

