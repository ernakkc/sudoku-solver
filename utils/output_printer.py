import os
import sys

def clear_console():
    """Clears the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')