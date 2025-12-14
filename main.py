from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QGridLayout,
                             QTextEdit, QScrollArea, QSpinBox, QMessageBox, QDialog, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QIcon, QCursor

import cv2
from datetime import datetime
from configparser import ConfigParser

from utils.style import main_style, FONTS
from utils import image2matrix
from utils.solving_algorithm import SudokuSAT
from utils.matrix2image import matrix_to_image
from utils.output_printer import OutputPrinterMixin
from utils.image_preprocessing import preprocess_sudoku_image

import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow, OutputPrinterMixin):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        icon_path = resource_path("media/icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.showFullScreen()
        
        self.setAnimated(True)
        self.setStyleSheet(main_style)

        # Use resource_path for all media files
        self.image_path = resource_path("media/icon.png")
        ai_png = resource_path("media/ai.png")
        # Use icon.png as default if ai.png doesn't exist
        self.processed_image_path = ai_png if os.path.exists(ai_png) else self.image_path
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

        # Right panel - Processed image with scroll area for multiple solutions
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
        
        # Scroll area for multiple solutions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container widget for solutions
        self.solutions_container = QWidget()
        self.solutions_layout = QGridLayout(self.solutions_container)
        self.solutions_layout.setSpacing(10)
        self.solutions_layout.setContentsMargins(10, 10, 10, 10)
        
        # Default image
        pixmap_processed = QPixmap(self.processed_image_path)
        self.processed_image_label = ClickableLabel()
        self.processed_image_label.setPixmap(pixmap_processed.scaled(480, 480, Qt.KeepAspectRatio))
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        self.processed_image_label.clicked.connect(lambda: self.show_image_popup(self.processed_image_path))
        self.solutions_layout.addWidget(self.processed_image_label, 0, 0)
        
        scroll_area.setWidget(self.solutions_container)
        
        right_frame_layout = QVBoxLayout(right_frame)
        right_frame_layout.setContentsMargins(0, 0, 0, 0)
        right_frame_layout.addWidget(scroll_area)
        
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
            self.processed_image_label.setPixmap(pixmap.scaled(480, 480, Qt.KeepAspectRatio))
            self.processed_image_label.update()
            self.processed_image_label.repaint()
            QApplication.processEvents()
            # Force multiple event loop cycles to ensure update
            QApplication.processEvents()
            QApplication.processEvents()
    
    def clear_solutions_panel(self):
        """Clear all solution images from the right panel"""
        # Remove all widgets except keep track of items to delete
        items_to_delete = []
        for i in range(self.solutions_layout.count()):
            item = self.solutions_layout.itemAt(i)
            if item and item.widget():
                items_to_delete.append(item.widget())
        
        # Delete all items
        for widget in items_to_delete:
            self.solutions_layout.removeWidget(widget)
            widget.deleteLater()
        
        # Recreate the default processed_image_label
        # Ensure the default image exists
        if not os.path.exists(self.processed_image_path):
            self.processed_image_path = "media/icon.png"
        
        pixmap_processed = QPixmap(self.processed_image_path)
        self.processed_image_label = ClickableLabel()
        if not pixmap_processed.isNull():
            self.processed_image_label.setPixmap(pixmap_processed.scaled(480, 480, Qt.KeepAspectRatio))
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        self.processed_image_label.clicked.connect(lambda: self.show_image_popup(self.processed_image_path))
        self.solutions_layout.addWidget(self.processed_image_label, 0, 0)
    
    def add_solution_image(self, image_path, solution_number, total_solutions):
        """Add a solution image to the grid layout"""
        # Create a frame for each solution
        solution_frame = QFrame()
        solution_frame.setObjectName("solutionFrame")
        solution_layout = QVBoxLayout(solution_frame)
        solution_layout.setContentsMargins(5, 5, 5, 5)
        solution_layout.setSpacing(5)
        
        # Solution label
        solution_label = QLabel(f"Solution {solution_number}/{total_solutions}")
        solution_label.setAlignment(Qt.AlignCenter)
        solution_label.setFont(QFont(FONTS['button'][0], 10, QFont.Bold))
        solution_layout.addWidget(solution_label)
        
        # Clickable image
        pixmap = QPixmap(image_path)
        image_label = ClickableLabel()
        image_label.setPixmap(pixmap.scaled(230, 230, Qt.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setCursor(QCursor(Qt.PointingHandCursor))
        image_label.clicked.connect(lambda: self.show_image_popup(image_path))
        solution_layout.addWidget(image_label)
        
        # Add to grid layout (2 columns)
        row = (solution_number - 1) // 2
        col = (solution_number - 1) % 2
        self.solutions_layout.addWidget(solution_frame, row, col)
    
    def show_image_popup(self, image_path):
        """Show image in a popup dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Sudoku Solution - Enlarged View")
        dialog.setModal(True)
        dialog.setMinimumSize(600, 600)
        
        layout = QVBoxLayout()
        
        pixmap = QPixmap(image_path)
        image_label = QLabel()
        image_label.setPixmap(pixmap.scaled(550, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        close_btn.setMinimumHeight(35)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def reset_image_previews(self):
        """Reset both image panels to their default state"""
        default_left = resource_path("media/icon.png")
        default_right = resource_path("media/ai.png")
        
        if os.path.exists(default_left):
            self.update_image_preview(default_left)
            self.image_path = default_left
        
        if os.path.exists(default_right):
            self.processed_image_path = default_right
        else:
            self.processed_image_path = default_left
            
        # Clear and recreate the solutions panel
        self.clear_solutions_panel()

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


    def solve_sudoku(self, image_path, skip_verification=False):
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
                self.print_info("Please try with a clearer image or different preprocessing.")
                return False
            
            # Validate matrix
            is_valid, error_msg = image2matrix.validate_matrix(sudoku_matrix)
            if not is_valid:
                self.print_error(f"Invalid matrix: {error_msg}")
                return False
            
            self.print_matrix(sudoku_matrix, "📋 Extracted Sudoku Puzzle")
            
            # Ask user if they want to edit the matrix (skip in batch mode)
            if not skip_verification:
                reply = QMessageBox.question(
                    self, 
                    'Verify Matrix', 
                    'Does the extracted puzzle look correct?\n\nClick "No" to manually edit the matrix.',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.No:
                    # Show matrix editor
                    sudoku_matrix = self.show_matrix_editor(sudoku_matrix)
                    if not sudoku_matrix:
                        self.print_info("❌ Matrix editing cancelled")
                        return False
                    self.print_success("✓ Matrix manually edited")
                    self.print_matrix(sudoku_matrix, "📋 Edited Sudoku Puzzle")
            else:
                self.print_info("⚡ Auto-mode: Skipping manual verification")

            # Step 3: Check if solvable
            self.print_info("Step 3/4: Checking if Sudoku is solvable...")
            solver = SudokuSAT()
            is_solvable, error_msg = solver.is_solvable(sudoku_matrix)
            
            if not is_solvable:
                self.print_error(f"{error_msg}")
                return False
            
            self.print_success("✓ Sudoku is valid and solvable!")
            
            # Step 4: Find all solutions
            self.print_info("Step 4/4: Computing solutions...")
            solver_multi = SudokuSAT()
            all_solutions = solver_multi.solve_all_sudoku(sudoku_matrix, max_solutions=10)
            
            if all_solutions:
                num_solutions = len(all_solutions)
                
                # Clear previous solutions
                self.clear_solutions_panel()
                
                if num_solutions == 1:
                    self.print_success(f"✓ Found UNIQUE solution (1/1)")
                    self.print_matrix(all_solutions[0], "🎯 Sudoku Solution")
                    
                    # Create and display single solution
                    solved_image = matrix_to_image(all_solutions[0], cell_size=52)
                    solved_image_path = "media/solved_sudoku.png"
                    solved_image.save(solved_image_path)
                    
                    # Update main display
                    pixmap = QPixmap(solved_image_path)
                    self.processed_image_label.setPixmap(pixmap.scaled(480, 480, Qt.KeepAspectRatio))
                    self.processed_image_label.image_path = solved_image_path
                    self.solutions_layout.addWidget(self.processed_image_label, 0, 0)
                    
                    self.processed_image_path = solved_image_path
                else:
                    self.print_warning(f"⚠️  Found MULTIPLE solutions: {num_solutions}")
                    self.print_info("Note: Well-designed Sudoku puzzles should have exactly 1 solution.")
                    self.print_info("")
                    
                    # Display all solutions
                    for idx, solution in enumerate(all_solutions, 1):
                        self.print_matrix(solution, f"🎯 Solution {idx}/{num_solutions}")
                        
                        # Create solution image
                        solved_image = matrix_to_image(solution, cell_size=52)
                        solved_image_path = f"media/solved_sudoku_{idx}.png"
                        solved_image.save(solved_image_path)
                        
                        # Add to grid
                        self.add_solution_image(solved_image_path, idx, num_solutions)
                        
                        self.print_success(f"✓ Solution {idx} image saved: {solved_image_path}")
                
                self.print_success("✓ All solutions displayed!")
                
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
        
        # Ask user about batch mode
        reply = QMessageBox.question(
            self,
            'Batch Processing Mode',
            'Enable automatic mode?\n\n'
            'YES = Skip manual verification for each file\n'
            'NO = Review each puzzle manually',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        batch_mode = (reply == QMessageBox.Yes)
        
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
                
                # Process the image (with batch mode setting)
                result = self.solve_sudoku(image_path, skip_verification=batch_mode)
                
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
        except KeyboardInterrupt:
            self.print_info("Camera capture interrupted by user (Ctrl+C)")
        except Exception as e:
            self.print_error(f"Camera error: {str(e)}")
        finally:
            if self.camera and self.camera.isOpened():
                self.camera.release()
            cv2.destroyAllWindows()
    
    def show_matrix_editor(self, matrix):
        """Show dialog to manually edit the Sudoku matrix"""
        dialog = QDialog(self)
        dialog.setWindowTitle("✏️ Edit Sudoku Matrix")
        dialog.setModal(True)
        dialog.setMinimumSize(500, 550)
        
        layout = QVBoxLayout()
        
        # Instructions
        info_label = QLabel("✏️ Edit the matrix below. Use 0 for empty cells, 1-9 for filled cells.")
        info_label.setFont(QFont(FONTS['section'][0], 12, QFont.Bold))
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # Create 9x9 grid of spinboxes
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(2)
        
        spinboxes = []
        for i in range(9):
            row_spinboxes = []
            for j in range(9):
                spinbox = QSpinBox()
                spinbox.setMinimum(0)
                spinbox.setMaximum(9)
                spinbox.setValue(matrix[i][j])
                spinbox.setAlignment(Qt.AlignCenter)
                spinbox.setMinimumWidth(45)
                spinbox.setMinimumHeight(45)
                spinbox.setFont(QFont(FONTS['button'][0], 12, QFont.Bold))
                
                # Add thick borders for 3x3 blocks
                if i % 3 == 0 and j % 3 == 0:
                    spinbox.setStyleSheet("border: 2px solid #00ff00; background-color: #1a1a1a; color: #00ff00;")
                elif i % 3 == 0 or j % 3 == 0:
                    spinbox.setStyleSheet("border: 1px solid #00cc00; background-color: #1a1a1a; color: #00ff00;")
                else:
                    spinbox.setStyleSheet("border: 1px solid #666; background-color: #1a1a1a; color: #00ff00;")
                
                grid_layout.addWidget(spinbox, i, j)
                row_spinboxes.append(spinbox)
            spinboxes.append(row_spinboxes)
        
        layout.addWidget(grid_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("✓ Apply Changes")
        ok_btn.setMinimumHeight(40)
        ok_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Extract values from spinboxes
            new_matrix = []
            for i in range(9):
                row = []
                for j in range(9):
                    row.append(spinboxes[i][j].value())
                new_matrix.append(row)
            return new_matrix
        else:
            return None
    


class ClickableLabel(QLabel):
    """Custom QLabel that emits a signal when clicked"""
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
