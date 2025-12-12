main_style = """
    /* Main Window - Dark Theme */
    QMainWindow {
        background-color: #0d0d0d;
    }
    
    /* Generic Labels */
    QLabel {
        color: #00ff00;
        background-color: transparent;
        font-family: 'Arial';
    }
    
    /* Main Title Label */
    QLabel#titleLabel {
        color: #00ff00;
        font-size: 60px;
        font-weight: bold;
        margin-bottom: 10px;
        font-family: 'Arial';
    }
    
    /* Section Title Labels (like "Original Image", "Processing Result", "Actions", "Console Output") */
    QLabel#sectionLabel {
        color: #00ff00;
        font-size: 16px;
        font-weight: bold;
        font-family: 'Arial';
    }
    
    /* Large Section Labels (like "Actions" label) */
    QLabel#largeActionLabel {
        color: #00ff00;
        font-size: 17px;
        font-weight: bold;
        font-family: 'Arial';
    }
    
    /* Console Title Label */
    QLabel#consoleLabel {
        color: #00ff00;
        font-size: 14px;
        font-weight: bold;
        font-family: 'Arial';
    }
    
    /* Push Buttons - Green Theme */
    QPushButton {
        background-color: #00cc00;
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 12px;
        font-weight: bold;
        font-family: 'Arial';
        min-height: 45px;
    }
    
    QPushButton:hover {
        background-color: #00ff00;
    }
    
    QPushButton:pressed {
        background-color: #009900;
    }
    
    /* Text Edit - Console Output */
    QTextEdit {
        background-color: #0d0d0d;
        border: 2px solid #00ff00;
        border-radius: 6px;
        padding: 10px;
        font-size: 10px;
        font-family: 'Courier';
        color: #00ff00;
        selection-background-color: #00cc00;
    }
    
    QTextEdit:focus {
        border: 2px solid #00ff00;
    }
    
    /* Line Edit */
    QLineEdit {
        background-color: #1a1a1a;
        border: 2px solid #00ff00;
        border-radius: 5px;
        padding: 8px;
        color: #00ff00;
        font-size: 11px;
        font-family: 'Courier';
    }
    
    QLineEdit:focus {
        border: 2px solid #00ff00;
        background-color: #0d0d0d;
    }
    
    /* Frames - Image Containers */
    QFrame#imageFrame {
        border: 3px solid #00ff00;
        border-radius: 8px;
        background-color: #1a1a1a;
        min-height: 520px;
        min-width: 520px;
    }
    
    QFrame#processedFrame {
        border: 3px solid #00ff00;
        border-radius: 8px;
        background-color: #1a1a1a;
        min-height: 520px;
        min-width: 520px;
    }
    
    /* Horizontal Separator */
    QFrame#separator {
        color: #00ff00;
        border: 2px solid #00ff00;
    }
    
    /* Scroll Area */
    QScrollArea {
        border: 2px solid #00ff00;
        border-radius: 6px;
        background-color: #0d0d0d;
    }
    
    QScrollArea:focus {
        border: 2px solid #00ff00;
    }
    
    /* Scroll Bars */
    QScrollBar:vertical {
        border: none;
        background-color: #1a1a1a;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #00cc00;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #00ff00;
    }
    
    QScrollBar:horizontal {
        border: none;
        background-color: #1a1a1a;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #00cc00;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #00ff00;
    }
    
    /* Combo Box */
    QComboBox {
        background-color: #1a1a1a;
        border: 2px solid #00ff00;
        border-radius: 5px;
        padding: 5px;
        color: #00ff00;
        font-size: 11px;
        font-family: 'Courier';
    }
    
    QComboBox:focus {
        border: 2px solid #00ff00;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #00ff00;
    }
    
    QComboBox::down-arrow {
        image: none;
        color: #00ff00;
    }
    
    /* Message Box */
    QMessageBox {
        background-color: #0d0d0d;
    }
    
    QMessageBox QLabel {
        color: #00ff00;
    }
    
    QMessageBox QPushButton {
        min-width: 60px;
    }
"""

# Font definitions for consistency
FONTS = {
    'title': ('Arial', 60, True),  # (family, size, bold)
    'section': ('Arial', 16, True),
    'large_action': ('Arial', 17, True),
    'console_label': ('Arial', 14, True),
    'button': ('Arial', 11, True),
    'console': ('Courier', 10, False),
}