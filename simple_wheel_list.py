#!/usr/bin/env python3
"""
Simple script to build and list wheel file contents.
"""

import subprocess
import sys
import zipfile
from pathlib import Path


def build_wheel():
    """Build a wheel file for the current project."""
    print("Building wheel...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "wheel", ".", "--wheel-dir", "dist", "--no-deps"], check=True)
        print("Wheel built successfully!")
        
        # Find the wheel file
        wheel_files = list(Path("dist").glob("*.whl"))
        return wheel_files[0] if wheel_files else None
    except subprocess.CalledProcessError as e:
        print(f"Error building wheel: {e}")
        return None


def list_wheel_files(wheel_path):
    """List all files in a wheel."""
    print(f"\nFiles in {wheel_path}:")
    print("-" * 50)
    
    with zipfile.ZipFile(wheel_path, 'r') as wheel:
        files = sorted(wheel.namelist())
        for file in files:
            print(file)
    
    print(f"\nTotal files: {len(files)}")
    return files


def main():
    # Build the wheel
    wheel_path = build_wheel()
    
    if wheel_path:
        # List the files
        files = list_wheel_files(wheel_path)
        
        # Save to text file
        with open("wheel_files_list.txt", "w") as f:
            f.write(f"Files in {wheel_path}:\n")
            f.write("-" * 50 + "\n")
            for file in files:
                f.write(f"{file}\n")
            f.write(f"\nTotal files: {len(files)}\n")
        
        print(f"\nFile list saved to: wheel_files_list.txt")
    else:
        print("Failed to build wheel")


if __name__ == "__main__":
    main()
