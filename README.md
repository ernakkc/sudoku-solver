# 🧩 Sudoku Solver

A powerful desktop application that solves Sudoku puzzles using image processing and SAT (Boolean Satisfiability) algorithms. Built with PyQt5 and powered by AI-based image recognition.

## ✨ Features

- **📁 Multiple Input Methods**
  - Solve from image files
  - Batch processing from folders
  - Real-time camera capture

- **🔍 Advanced Image Processing**
  - Automatic Sudoku grid detection
  - Cell extraction and digit recognition
  - Preprocessing pipeline with step-by-step visualization

- **🧠 Smart Solving Algorithm**
  - SAT-based solving using Boolean constraints
  - Fast and reliable solutions
  - Validation of solvable puzzles

- **🎨 Modern GUI**
  - Full-screen desktop application
  - Real-time preview of original and processed images
  - Console output for detailed logs

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd app
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API settings:
   - Copy `config.ini.example` to `config.ini`
   - Add your Google Generative AI API key:
   ```ini
   [GENAI]
   API_KEY = your_api_key_here
   ```

## 📖 Usage

### Running the Application

```bash
python main.py
```

### Solving Sudoku Puzzles

1. **From File**: Click "📁 Solve from File" and select an image containing a Sudoku puzzle
2. **From Folder**: Click "📂 Solve from Folder" to batch process multiple Sudoku images
3. **From Camera**: Click "📷 Solve from Camera" to capture a Sudoku puzzle in real-time

### Supported Image Formats

- PNG
- JPG/JPEG
- Images should clearly show a 9×9 Sudoku grid

## 🛠️ Technologies Used

- **PyQt5**: Desktop GUI framework
- **OpenCV**: Image processing and computer vision
- **Google Generative AI**: Digit recognition from grid cells
- **Python-SAT**: Boolean satisfiability solver for Sudoku logic
- **NumPy & Pandas**: Data manipulation

## 📁 Project Structure

```
app/
├── main.py                    # Main application entry point
├── config.ini                 # Configuration file (not tracked)
├── requirements.txt           # Python dependencies
├── media/                     # Application assets
│   └── icon.png              # Application icon
├── sudoku_examples/          # Sample Sudoku images
├── utils/                    # Utility modules
│   ├── image_preprocessing.py    # Image processing pipeline
│   ├── image2matrix.py          # Grid extraction and OCR
│   ├── matrix2image.py          # Solution visualization
│   ├── solving_algorithm.py     # SAT-based solver
│   ├── output_printer.py        # Console output handler
│   ├── style.py                 # GUI styling
│   └── check_requirements.py   # Dependency checker
└── preprocessing_steps/      # Debug images (not tracked)
```

## 🎯 How It Works

1. **Image Preprocessing**: The input image is preprocessed to detect and extract the Sudoku grid
2. **Cell Extraction**: Each cell in the 9×9 grid is isolated
3. **Digit Recognition**: Google's Generative AI identifies digits in each cell
4. **SAT Solving**: The puzzle is converted to Boolean constraints and solved using a SAT solver
5. **Visualization**: The solution is overlaid on the original image

## 📝 Example Puzzles

Sample Sudoku images are provided in the `sudoku_examples/` folder for testing.

## ⚠️ Troubleshooting

- **API Key Error**: Make sure your Google Generative AI API key is correctly set in `config.ini`
- **Image Recognition Issues**: Ensure the image is clear and well-lit with a visible grid
- **Missing Dependencies**: Run `pip install -r requirements.txt` again

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is developed as part of a Discrete Mathematics course project.

## 👥 Authors

Developed for the Discrete Mathematics course at university.

---

**Note**: This application requires an active internet connection for digit recognition via Google's Generative AI API.
