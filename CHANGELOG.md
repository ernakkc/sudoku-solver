# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-19

### Added
- Initial release of Sudoku Solver desktop application
- Image processing pipeline for Sudoku grid detection
- AI-powered digit recognition using Google Gemini 2.0 Flash Exp
- SAT-based solving algorithm with multiple solution detection
- Interactive GUI with PyQt5
- Manual matrix editing interface
- Batch processing from folders
- Real-time camera capture
- Multiple solution display with grid layout
- Comprehensive image preprocessing steps
- Build scripts for executable generation

### Features
- Solve Sudoku from image files, folders, or camera
- Automatic grid detection and cell extraction
- User verification and manual editing
- Multiple solution finding (up to 10 solutions)
- Visual solution display with clickable thumbnails
- Console logging for debugging
- Cross-platform executable builds

### Technical
- PyQt5 for desktop GUI
- OpenCV for image processing
- Google Generative AI for OCR
- Python-SAT (Glucose3) for constraint solving
- PIL/Pillow for image manipulation