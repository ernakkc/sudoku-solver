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

import cv2
from time import sleep
from random import randint
from configparser import ConfigParser

from utils.style import main_style, FONTS
from utils import image2matrix
from utils.solving_algorithm import SudokuSAT
from utils.matrix2image import matrix_to_image
from utils.output_printer import OutputPrinterMixin
from utils.image_preprocessing import preprocess_sudoku_image

import sys
import os


class MainWindow(QMainWindow, OutputPrinterMixin):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setWindowIcon(QIcon("media/icon.png"))
        
        # Set to full screen
        self.showFullScreen()
        
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
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # CAPTION LABEL
        label = QLabel("🧩 SUDOKU SOLVER")
        label.setObjectName("titleLabel")
        label.setFont(QFont(FONTS['title'][0], FONTS['title'][1], QFont.Bold if FONTS['title'][2] else QFont.Normal))
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        # SEPARATOR
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)

        # IMAGE PREVIEW SECTION
        image_section = QHBoxLayout()
        image_section.setSpacing(20)

        # Left panel - Original image
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_label = QLabel("📷 Original Image")
        left_label.setObjectName("sectionLabel")
        left_label.setFont(QFont(FONTS['section'][0], FONTS['section'][1], QFont.Bold if FONTS['section'][2] else QFont.Normal))
        left_layout.addWidget(left_label)
        
        left_frame = QFrame()
        left_frame.setObjectName("imageFrame")
        left_frame.setMinimumHeight(520)
        left_frame.setMinimumWidth(520)
        left_inner = QVBoxLayout(left_frame)
        left_inner.setContentsMargins(10, 10, 10, 10)
        
        pixmap = QPixmap(self.image_path)
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap.scaled(480, 480, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        left_inner.addWidget(self.image_label)
        
        left_layout.addWidget(left_frame)
        left_layout.addStretch()
        image_section.addWidget(left_panel)

        # Right panel - Processed image
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_label = QLabel("🧩 Processing Result")
        right_label.setObjectName("sectionLabel")
        right_label.setFont(QFont(FONTS['section'][0], FONTS['section'][1], QFont.Bold if FONTS['section'][2] else QFont.Normal))
        right_layout.addWidget(right_label)
        
        right_frame = QFrame()
        right_frame.setObjectName("processedFrame")
        right_frame.setMinimumHeight(520)
        right_frame.setMinimumWidth(520)
        right_inner = QVBoxLayout(right_frame)
        right_inner.setContentsMargins(10, 10, 10, 10)
        
        pixmap_processed = QPixmap(self.processed_image_path)
        self.processed_image_label = QLabel()
        self.processed_image_label.setPixmap(pixmap_processed.scaled(480, 480, Qt.KeepAspectRatio))
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        right_inner.addWidget(self.processed_image_label)
        
        right_layout.addWidget(right_frame)
        right_layout.addStretch()
        image_section.addWidget(right_panel)

        main_layout.addLayout(image_section, 2)

        # BOTTOM SECTION - Controls and Terminal
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Buttons panel
        buttons_panel = QWidget()
        buttons_layout = QVBoxLayout(buttons_panel)
        buttons_layout.setSpacing(12)
        
        buttons_label = QLabel("📋 Actions")
        buttons_label.setObjectName("largeActionLabel")
        buttons_label.setFont(QFont(FONTS['large_action'][0], FONTS['large_action'][1], QFont.Bold if FONTS['large_action'][2] else QFont.Normal))
        buttons_layout.addWidget(buttons_label)

        solve_from_file_button = QPushButton("📁 Solve from File")
        solve_from_file_button.setFont(QFont(FONTS['button'][0], FONTS['button'][1], QFont.Bold if FONTS['button'][2] else QFont.Normal))
        solve_from_file_button.setMinimumHeight(45)
        solve_from_file_button.clicked.connect(self.on_file_button_click)
        buttons_layout.addWidget(solve_from_file_button)

        solve_from_folder_button = QPushButton("📂 Solve from Folder")
        solve_from_folder_button.setFont(QFont(FONTS['button'][0], FONTS['button'][1], QFont.Bold if FONTS['button'][2] else QFont.Normal))
        solve_from_folder_button.setMinimumHeight(45)
        solve_from_folder_button.clicked.connect(self.on_folder_button_click)
        buttons_layout.addWidget(solve_from_folder_button)

        solve_from_camera_button = QPushButton("📷 Solve from Camera")
        solve_from_camera_button.setFont(QFont(FONTS['button'][0], FONTS['button'][1], QFont.Bold if FONTS['button'][2] else QFont.Normal))
        solve_from_camera_button.setMinimumHeight(45)
        solve_from_camera_button.clicked.connect(self.on_camera_button_click)
        buttons_layout.addWidget(solve_from_camera_button)
        
        buttons_layout.addStretch()
        buttons_panel.setMaximumWidth(280)
        bottom_layout.addWidget(buttons_panel)

        # Terminal Output
        terminal_panel = QWidget()
        terminal_layout = QVBoxLayout(terminal_panel)
        
        terminal_label = QLabel("📊 Console Output")
        terminal_label.setObjectName("consoleLabel")
        terminal_label.setFont(QFont(FONTS['console_label'][0], FONTS['console_label'][1], QFont.Bold if FONTS['console_label'][2] else QFont.Normal))
        terminal_layout.addWidget(terminal_label)
        
        self.result_text_edit = QTextEdit()
        self.result_text_edit.setText("--- Sudoku Solver Console ---\n\n")
        self.result_text_edit.setMinimumHeight(280)
        self.result_text_edit.setReadOnly(True)
        self.result_text_edit.setFont(QFont(FONTS['console'][0], FONTS['console'][1], QFont.Bold if FONTS['console'][2] else QFont.Normal))
        terminal_layout.addWidget(self.result_text_edit)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        
        bottom_layout.addWidget(terminal_panel, 1)
        bottom_layout.setStretchFactor(buttons_panel, 0)
        bottom_layout.setStretchFactor(terminal_panel, 1)

        main_layout.addLayout(bottom_layout, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def update_image_preview(self, image_path):
        if not image_path:
            return
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio))
            self.image_label.repaint()
            QApplication.processEvents()
    
    def update_processed_image_preview(self, image_path):
        if not image_path:
            return
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.processed_image_label.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio))
            self.processed_image_label.update()
            self.processed_image_label.repaint()
            QApplication.processEvents()
            # Force multiple event loop cycles to ensure update
            QApplication.processEvents()
            QApplication.processEvents()

    def reset_image_previews(self):
        """Reset both image panels to their default state"""
        default_left = "media/icon.png"
        default_right = "media/ai.png"
        
        if os.path.exists(default_left):
            self.update_image_preview(default_left)
            self.image_path = default_left
        
        if os.path.exists(default_right):
            self.update_processed_image_preview(default_right)
            self.processed_image_path = default_right

    def on_button_click(self):
        QMessageBox.information(self, "Information", "Button Clicked!")     
        self.print_info("Button clicked")

    def on_file_button_click(self):
        # Reset image previews to default state
        self.reset_image_previews()
        
        self.print_section("SUDOKU SOLVER - FROM FILE")
        
        # Open file dialog to select an image file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Sudoku Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)
        if file_name:
            self.print_success(f"File selected: {file_name.split('/')[-1]}")
            # Update the image preview
            self.update_image_preview(file_name)
            self.image_path = file_name
            self.mode = "file"

            self.solve_sudoku(self.image_path)

    def on_folder_button_click(self):
        # Reset image previews to default state
        self.reset_image_previews()
        
        self.printT("\nSolve from Folder button was clicked at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # Open folder dialog to select a folder
        options = QFileDialog.Options()
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder Containing Sudoku Images", options=options)
        if folder_name:
            self.printT(f"Selected folder: {folder_name.split('/')[-1]}")
            self.mode = "folder"
            self.solve_sudokus_in_folder(folder_path=folder_name)

    def on_camera_button_click(self):
        # Reset image previews to default state
        self.reset_image_previews()
        
        self.print_section("SUDOKU SOLVER - FROM CAMERA")
        self.print_info("Starting camera capture...")
        self.solve_sudoku_from_camera()


    def solve_sudoku(self, image_path):
        try:
            self.print_info(f"Processing image: {image_path.split('/')[-1]}")
            
            # Step 1: Preprocess the image
            self.print_info("Step 1/4: Preprocessing image...")
            processed_image, preprocessing_steps = preprocess_sudoku_image(
                image_path, 
                update_callback=self.update_processed_image_preview
            )
            
            # Display preprocessing steps
            self.print_info(f"✓ Image preprocessing completed with {len(preprocessing_steps)} steps")
            
            # Save processed image for Gemini
            processed_image_path = "temp_processed_sudoku.png"
            cv2.imwrite(processed_image_path, processed_image)

            # Step 2: Extract Sudoku matrix
            self.print_info("Step 2/4: Extracting Sudoku grid from preprocessed image...")
            sudoku_matrix = image2matrix.with_gemini(self.API_KEY, processed_image_path)
            if not sudoku_matrix:
                self.print_error("Failed to extract Sudoku grid from image!")
                return False
            
            self.print_matrix(sudoku_matrix, "📋 Extracted Sudoku Puzzle")

            # Step 3: Check if solvable
            self.print_info("Step 3/4: Checking if Sudoku is solvable...")
            solver = SudokuSAT()
            is_solvable, error_msg = solver.is_solvable(sudoku_matrix)
            
            if not is_solvable:
                self.print_error(f"{error_msg}")
                return False
            
            self.print_success("✓ Sudoku is valid and solvable!")
            
            # Step 4: Solve the puzzle
            self.print_info("Step 4/4: Computing solution...")
            solver = SudokuSAT()
            solution = solver.solve_sudoku(sudoku_matrix)
            
            if solution:
                self.print_matrix(solution, "🎯 Sudoku Solution")
                self.print_success("✓ Sudoku solved successfully!")

                # create solution image
                solved_image = matrix_to_image(solution, cell_size=52)
                solved_image_path = "media/solved_sudoku.png"
                solved_image.save(solved_image_path)
                self.update_processed_image_preview(solved_image_path)
                self.print_success(f"✓ Solution image saved: {solved_image_path}")

                self.processed_image_path = solved_image_path
                
                # Show preprocessing steps location
                if preprocessing_steps:
                    steps_dir = os.path.dirname(preprocessing_steps[0][1])
                    self.print_info(f"📁 Preprocessing steps saved in: {steps_dir}")
                
                self.print_section("✨ PROCESS COMPLETED ✨")
                return True
            else:
                self.print_error("Error solving Sudoku")
                return False
        except Exception as e:
            self.print_error(f"Unexpected error: {str(e)}")
            return False

    def solve_sudokus_in_folder(self, folder_path):
        self.print_section("SUDOKU SOLVER - FROM FOLDER")
        self.print_info(f"Processing Sudoku puzzles from folder: {folder_path.split('/')[-1]}")
        
        file_count = 0
        successful_count = 0
        failed_count = 0
        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                file_count += 1
                image_path = os.path.join(folder_path, filename)
                
                self.print_section(f"📄 FILE [{file_count}]: {filename}")
                
                # Display original image
                self.update_image_preview(image_path)
                
                # Process the image
                result = self.solve_sudoku(image_path)
                
                if result:
                    successful_count += 1
                    self.print_success(f"✓ {filename} - Successfully solved!")
                else:
                    failed_count += 1
                    self.print_error(f"✗ {filename} - Failed to solve!")
                
                # Add separator between files
                self.print_info("─" * 60)
        
        # Summary
        if file_count == 0:
            self.print_error("No image files found in folder!")
        else:
            self.print_section(f"📊 FOLDER PROCESSING SUMMARY")
            self.print_info(f"Total files processed: {file_count}")
            self.print_success(f"Successfully solved: {successful_count}")
            if failed_count > 0:
                self.print_error(f"Failed to solve: {failed_count}")
            self.print_section(f"✨ BATCH PROCESSING COMPLETED ✨")

    def solve_sudoku_from_camera(self):
        """Capture Sudoku image from camera and solve it"""
        self.camera = cv2.VideoCapture(0)
        
        if not self.camera.isOpened():
            self.print_error("Camera not available or could not be opened!")
            return
        
        self.print_info("Camera opened successfully")
        self.print_info("Controls: SPACE=Capture | ESC=Cancel")
        
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    self.print_error("Failed to grab frame from camera.")
                    break

                # Flip frame for mirror effect (Y-axis flip)
                 # frame = cv2.flip(frame, 0)
                
                # Add text overlay
                cv2.putText(frame, "SUDOKU CAMERA CAPTURE", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "SPACE: Capture | ESC: Cancel", (20, 80),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow("Sudoku Camera - Capture Mode", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    self.print_info("Camera capture cancelled by user")
                    break
                elif key == 32:  # SPACE
                    # Capture the image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    captured_image_path = f"media/captured_sudoku_{timestamp}.png"
                    cv2.imwrite(captured_image_path, frame)
                    self.print_success(f"Image captured: {captured_image_path}")
                    
                    # Update preview
                    self.update_image_preview(captured_image_path)
                    self.image_path = captured_image_path
                    self.mode = "camera"
                    
                    # Close camera window and solve
                    self.camera.release()
                    cv2.destroyAllWindows()
                    
                    # Process the captured image
                    QApplication.processEvents()  # Allow UI to update
                    self.solve_sudoku(captured_image_path)
                    break
        except Exception as e:
            self.print_error(f"Camera error: {str(e)}")
        finally:
            if self.camera and self.camera.isOpened():
                self.camera.release()
            cv2.destroyAllWindows()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
