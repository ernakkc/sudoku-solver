#!/usr/bin/env python3
"""
Sudoku Solver - Build Script
Generates executable files for macOS and Windows using PyInstaller
"""

import os
import sys
import platform
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller not found")
        print("\nInstalling PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True

def clean_build_files():
    """Remove old build files"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['main.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}/")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✓ Removed {file_name}")

def convert_icon():
    """Convert PNG icon to platform-specific format"""
    icon_path = "media/icon.png"
    
    if not os.path.exists(icon_path):
        print(f"✗ Icon not found: {icon_path}")
        return None
    
    system = platform.system()
    
    if system == "Windows":
        # Convert PNG to ICO for Windows
        try:
            from PIL import Image
            img = Image.open(icon_path)
            ico_path = "media/icon.ico"
            img.save(ico_path, format='ICO', sizes=[(256, 256)])
            print(f"✓ Created Windows icon: {ico_path}")
            return ico_path
        except Exception as e:
            print(f"⚠ Could not create .ico file: {e}")
            return icon_path
    
    elif system == "Darwin":  # macOS
        # Convert PNG to ICNS for macOS
        icns_path = "media/icon.icns"
        
        try:
            # Create iconset directory
            iconset_dir = "media/icon.iconset"
            os.makedirs(iconset_dir, exist_ok=True)
            
            from PIL import Image
            img = Image.open(icon_path)
            
            # Generate required icon sizes for macOS
            sizes = [16, 32, 64, 128, 256, 512]
            for size in sizes:
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                resized.save(f"{iconset_dir}/icon_{size}x{size}.png")
                # Retina versions
                resized_2x = img.resize((size * 2, size * 2), Image.Resampling.LANCZOS)
                resized_2x.save(f"{iconset_dir}/icon_{size}x{size}@2x.png")
            
            # Convert iconset to icns using macOS tool
            subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', icns_path], 
                         check=True, capture_output=True)
            
            # Cleanup iconset
            shutil.rmtree(iconset_dir)
            
            print(f"✓ Created macOS icon: {icns_path}")
            return icns_path
        except Exception as e:
            print(f"⚠ Could not create .icns file: {e}")
            return icon_path
    
    return icon_path

def build_executable():
    """Build the executable using PyInstaller"""
    
    print("\n" + "="*50)
    print("  SUDOKU SOLVER - BUILD SCRIPT")
    print("="*50 + "\n")
    
    # Check PyInstaller
    if not check_pyinstaller():
        return False
    
    # Clean old builds
    print("\n📁 Cleaning old build files...")
    clean_build_files()
    
    # Convert icon
    print("\n🎨 Preparing application icon...")
    icon_path = convert_icon()
    
    # Detect platform
    system = platform.system()
    print(f"\n💻 Detected platform: {system}")
    
    # Build command
    app_name = "SudokuSolver"
    
    pyinstaller_args = [
        'pyinstaller',
        '--name', app_name,
        '--onefile',  # Single file executable
        '--windowed',  # No console window
        '--clean',
    ]
    
    # Add icon if available
    if icon_path:
        pyinstaller_args.extend(['--icon', icon_path])
    
    # Add data files (media folder, config.ini template, etc.)
    pyinstaller_args.extend([
        '--add-data', f'media{os.pathsep}media',
        '--add-data', f'utils{os.pathsep}utils',
        '--add-data', f'config.ini{os.pathsep}.',
    ])
    
    # Hidden imports (sometimes needed for PyQt5)
    pyinstaller_args.extend([
        '--hidden-import', 'PyQt5',
        '--hidden-import', 'PIL',
        '--hidden-import', 'cv2',
        '--hidden-import', 'pysat',
        # Exclude conflicting Qt packages
        '--exclude-module', 'PySide6',
        '--exclude-module', 'PySide2',
        '--exclude-module', 'PyQt6',
        # Exclude unnecessary packages to reduce size
        '--exclude-module', 'matplotlib',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'IPython',
        '--exclude-module', 'pytest',
        '--exclude-module', 'jedi',
    ])
    
    # Main script
    pyinstaller_args.append('main.py')
    
    # Build
    print("\n🔨 Building executable...")
    print(f"Command: {' '.join(pyinstaller_args)}\n")
    
    try:
        subprocess.check_call(pyinstaller_args)
        print("\n✅ Build completed successfully!")
        
        # Show output location
        if system == "Windows":
            exe_path = f"dist/{app_name}.exe"
            print(f"\n📦 Executable created: {exe_path}")
            print(f"   Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
        elif system == "Darwin":
            app_path = f"dist/{app_name}.app"
            print(f"\n📦 Application created: {app_path}")
            if os.path.exists(app_path):
                # Calculate app bundle size
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(app_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                print(f"   Size: {total_size / (1024*1024):.1f} MB")
        else:
            exe_path = f"dist/{app_name}"
            print(f"\n📦 Executable created: {exe_path}")
        
        print("\n📋 Build artifacts:")
        print("   - dist/          → Your executable is here!")
        print("   - build/         → Temporary build files (can be deleted)")
        print("   - main.spec      → PyInstaller spec file (can be deleted)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    success = build_executable()
    
    if success:
        print("\n" + "="*50)
        print("  ✨ BUILD SUCCESSFUL! ✨")
        print("="*50)
        print("\nYour executable is ready in the 'dist/' folder!")
        print("\nTo distribute:")
        print("  • Windows: Share the .exe file")
        print("  • macOS:   Share the .app bundle")
        print("\nNote: Users will need to place config.ini in the same")
        print("      directory as the executable with their API key.")
    else:
        print("\n" + "="*50)
        print("  ❌ BUILD FAILED")
        print("="*50)
        sys.exit(1)
