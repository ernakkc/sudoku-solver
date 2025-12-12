import sys

def check_requirements():
    required_packages = []

    with open('requirements.txt', 'r') as f:
        for line in f:
            package = line.strip().split('==')[0]
            required_packages.append(package)

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError as E:
            missing_packages.append(package)
            print(f"Package '{package}' is missing: {E}")

    if not missing_packages:
        print("All required packages are installed.")
        return True
    
    print("Missing packages:")
    for pkg in missing_packages:
        print(f"- {pkg}")
    print("\n Installing missing packages...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])
        print("Missing packages installed successfully.")
        return True
    except Exception as e:
        print(f"Failed to install packages: {e}")
        return False

