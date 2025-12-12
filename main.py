from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTableWidget, QTabWidget,
                             QTableWidgetItem, QHeaderView, QFrame, QGridLayout,
                             QTextEdit, QLineEdit, QComboBox, QDateEdit, QTimeEdit,
                             QScrollArea, QSplitter, QGroupBox, QSpinBox, QCheckBox,
                             QProgressBar, QListWidget, QListWidgetItem, QMessageBox, QDialog,
                             QCalendarWidget, QAbstractItemView, QDoubleSpinBox, QFileDialog)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from datetime import datetime, timedelta


from time import sleep
from random import randint
from configparser import ConfigParser

from utils.style import main_style
from utils import image2matrix

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setWindowIcon(QIcon("media/icon.png"))
        self.setGeometry(100, 100, 1200, 800)
        self.setAnimated(True)
        self.setStyleSheet(main_style)


        # INITIALIZE VARIABLES
        self.image_path = "media/icon.png"
        self.processed_image_path = "media/ai.png"
        self.images = []
        self.camera = None
        self.mode = None

        config = ConfigParser()
        config.read('config.ini')
        self.API_KEY = config.get('GENAI', 'API_KEY')

        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()


        # CAPTION LABEL
        label = QLabel("Sudoku Solver")
        label.setFont(QFont("Arial", 50, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)


        # IMAGE PREVIEW
        image_layout = QHBoxLayout()

        # preview image 
        pixmap = QPixmap(self.image_path)
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_label)

        # processed image placeholder
        pixmap_processed = QPixmap(self.processed_image_path)
        self.processed_image_label = QLabel()
        self.processed_image_label.setPixmap(pixmap_processed.scaled(400, 400, Qt.KeepAspectRatio))
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.processed_image_label) 
        

        # SOLVE BUTTONS
        solve_result_layout = QHBoxLayout()
        solve_layout = QVBoxLayout()

        solve_layout.addStretch()

        solve_from_file_button = QPushButton("Solve from File")
        solve_from_file_button.setMinimumWidth(350)
        solve_from_file_button.clicked.connect(self.on_file_button_click)
        solve_layout.addWidget(solve_from_file_button)

        solve_from_folder_button = QPushButton("Solve from Folder")
        solve_from_folder_button.clicked.connect(self.on_button_click)
        solve_layout.addWidget(solve_from_folder_button)

        solve_from_camera_button = QPushButton("Solve from Camera")
        solve_from_camera_button.clicked.connect(self.on_button_click)
        solve_layout.addWidget(solve_from_camera_button)

        
        # Terminal Output
        result_terminal_layout = QVBoxLayout()
        result_label = QLabel("Result Terminal")
        result_label.setFont(QFont("Arial", 20, QFont.Bold))
        result_label.setAlignment(Qt.AlignCenter)
        result_terminal_layout.addWidget(result_label)
        self.result_text_edit = QTextEdit()
        self.result_text_edit.setText("--- Result Terminal ---\n")
        self.result_text_edit.setMinimumWidth(800)
        self.result_text_edit.setReadOnly(True)
        result_terminal_layout.addWidget(self.result_text_edit)


        solve_result_layout.addLayout(solve_layout)
        solve_result_layout.addStretch()
        solve_result_layout.addLayout(result_terminal_layout)
        

        main_layout.addWidget(label)
        main_layout.addLayout(image_layout)
        main_layout.addStretch()
        main_layout.addLayout(solve_result_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_button_click(self):
        QMessageBox.information(self, "Information", "Button Clicked!")     
        self.printT("Button was clicked at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def printT(self, message):  
        for char in message:
            self.result_text_edit.moveCursor(self.result_text_edit.textCursor().End)
            self.result_text_edit.insertPlainText(char)
            QApplication.processEvents() 
            sleep(randint(1,3)/50) 
        self.result_text_edit.insertPlainText("\n")
        print(message)

    def on_file_button_click(self):
        self.printT("\nSolve from File button was clicked at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Open file dialog to select an image file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Sudoku Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)
        if file_name:
            self.printT(f"Selected file: {file_name.split('/')[-1]}")
            # Update the image preview
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(500 , 500, Qt.KeepAspectRatio))
            self.image_path = file_name
            self.mode = "file"

            self.solve_sudoku(self.image_path)

    def solve_sudoku(self, image_path):
        self.printT(f"Solving Sudoku for image: {image_path.split('/')[-1]}")
        # image to matrix
        self.printT("Processing image and extracting Sudoku grid...")
        sudoku_matrix = image2matrix.with_gemini(self.API_KEY, image_path)
        if sudoku_matrix:
            self.printT("Extracted Sudoku Matrix:")
            for row in sudoku_matrix:
                self.printT(str(row))
        else:
            self.printT("Failed to extract Sudoku matrix from the image.")
            return

        # Here you would add the code to process the image and solve the Sudoku puzzle
        self.printT("Sudoku solved successfully! (This is a placeholder message)")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
