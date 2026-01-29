# build.py
import os
import shutil
import subprocess
import sys


def install_package(package):
    """Install a package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def build_exe():
    """Build the EXE file using PyInstaller"""
    print("Building MonkeyPox Detector EXE...")

    # Check if PyInstaller is installed
    try:
        import pyinstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        install_package("pyinstaller")

    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    # Build command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "MonkeyPox_Detector",
        "--add-data", "predictions.csv;.",  # Include data files
        "main.py"
    ]

    # Run PyInstaller
    subprocess.check_call(cmd)

    print("Build complete!")
    print("The EXE file is located in the 'dist' folder.")


if __name__ == "__main__":
    build_exe()