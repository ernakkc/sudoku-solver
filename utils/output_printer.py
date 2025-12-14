import os
import sys
from time import sleep
from random import randint
from PyQt5.QtWidgets import QApplication

def clear_console():
    """Clears the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')


class OutputPrinterMixin:
    """Mixin class for adding formatted output methods to GUI applications"""
    
    def printT(self, message):  
        """Typewriter effect print to result_text_edit"""
        for char in message:
            self.result_text_edit.moveCursor(self.result_text_edit.textCursor().End)
            self.result_text_edit.insertPlainText(char)
            QApplication.processEvents() 
            sleep(randint(1,15)/1000) 
        self.result_text_edit.insertPlainText("\n")
        print(message)
    
    def print_section(self, title):
        """Print section header with separator"""
        separator = "═" * 30
        self.printT(f"\n{separator}")
        self.printT(f"  {title}")
        self.printT(f"{separator}")
    
    def print_matrix(self, matrix, title="Matrix"):
        """Print 9x9 matrix in formatted grid"""
        self.printT(f"\n{title}:")
        for i, row in enumerate(matrix):
            if i % 3 == 0 and i != 0:
                self.printT("  " + "─" * 21)
            row_str = "  "
            for j, val in enumerate(row):
                if j % 3 == 0 and j != 0:
                    row_str += "│ "
                row_str += f"{val} "
            self.printT(row_str)
    
    def print_success(self, message):
        """Print success message with checkmark"""
        self.printT(f"✓ {message}")
    
    def print_error(self, message):
        """Print error message with X mark"""
        self.printT(f"✗ {message}")
    
    def print_info(self, message):
        """Print info message with info icon"""
        self.printT(f"ℹ {message}")
    
    def print_warning(self, message):
        """Print warning message with warning icon"""
        self.printT(f"⚠️  {message}")