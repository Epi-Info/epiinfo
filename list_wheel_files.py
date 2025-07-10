#!/usr/bin/env python3
"""
Script to build a wheel file and list all files contained within it.

This script can:
1. Build a wheel file for the current project
2. List all files in an existing wheel file
3. Extract detailed information about wheel contents
"""

import os
import sys
import subprocess
import zipfile
import argparse
from pathlib import Path
import tempfile
import shutil


def build_wheel(output_dir="dist"):
    """Build a wheel file for the current project."""
    print("Building wheel file...")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Build the wheel using pip
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "wheel", ".", 
            "--wheel-dir", output_dir, "--no-deps"
        ], capture_output=True, text=True, check=True)
        
        print("Wheel build completed successfully!")
        print(f"Output: {result.stdout}")
        
        # Find the generated wheel file
        wheel_files = list(Path(output_dir).glob("*.whl"))
        if wheel_files:
            return wheel_files[0]  # Return the first wheel file found
        else:
            print("No wheel file found after build.")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"Error building wheel: {e}")
        print(f"stderr: {e.stderr}")
        return None


def list_wheel_contents(wheel_path, detailed=False, save_to_file=None):
    """
    List all files in a wheel file.
    
    Args:
        wheel_path: Path to the wheel file
        detailed: If True, show detailed information about each file
        save_to_file: If provided, save the list to this file
    """
    wheel_path = Path(wheel_path)
    
    if not wheel_path.exists():
        print(f"Wheel file not found: {wheel_path}")
        return []
    
    print(f"\nContents of wheel file: {wheel_path.name}")
    print("=" * 60)
    
    files_list = []
    
    try:
        with zipfile.ZipFile(wheel_path, 'r') as wheel_zip:
            file_info_list = wheel_zip.infolist()
            
            # Sort files by name for better readability
            file_info_list.sort(key=lambda x: x.filename)
            
            for file_info in file_info_list:
                if detailed:
                    # Show detailed information
                    size = file_info.file_size
                    compressed_size = file_info.compress_size
                    compression_ratio = (1 - compressed_size / size) * 100 if size > 0 else 0
                    
                    file_details = {
                        'filename': file_info.filename,
                        'size': size,
                        'compressed_size': compressed_size,
                        'compression_ratio': compression_ratio,
                        'date_time': file_info.date_time
                    }
                    files_list.append(file_details)
                    
                    print(f"{file_info.filename:<50} {size:>8} bytes "
                          f"({compressed_size:>8} compressed, {compression_ratio:>5.1f}% saved)")
                else:
                    files_list.append(file_info.filename)
                    print(file_info.filename)
            
            print(f"\nTotal files: {len(file_info_list)}")
            
            if detailed:
                total_size = sum(f['size'] for f in files_list)
                total_compressed = sum(f['compressed_size'] for f in files_list)
                overall_ratio = (1 - total_compressed / total_size) * 100 if total_size > 0 else 0
                print(f"Total size: {total_size:,} bytes")
                print(f"Compressed size: {total_compressed:,} bytes")
                print(f"Overall compression: {overall_ratio:.1f}%")
    
    except zipfile.BadZipFile:
        print(f"Error: {wheel_path} is not a valid zip/wheel file")
        return []
    except Exception as e:
        print(f"Error reading wheel file: {e}")
        return []
    
    # Save to file if requested
    if save_to_file:
        save_list_to_file(files_list, save_to_file, detailed)
    
    return files_list


def save_list_to_file(files_list, output_file, detailed=False):
    """Save the files list to a text file."""
    output_path = Path(output_file)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Wheel File Contents\n")
            f.write(f"Generated on: {Path().absolute()}\n")
            f.write("=" * 60 + "\n\n")
            
            if detailed and files_list and isinstance(files_list[0], dict):
                # Write detailed format
                f.write(f"{'Filename':<50} {'Size':<10} {'Compressed':<10} {'Saved':<8}\n")
                f.write("-" * 80 + "\n")
                
                for file_info in files_list:
                    f.write(f"{file_info['filename']:<50} "
                           f"{file_info['size']:<10} "
                           f"{file_info['compressed_size']:<10} "
                           f"{file_info['compression_ratio']:<8.1f}%\n")
                
                total_size = sum(f['size'] for f in files_list)
                total_compressed = sum(f['compressed_size'] for f in files_list)
                overall_ratio = (1 - total_compressed / total_size) * 100 if total_size > 0 else 0
                
                f.write("\n" + "-" * 80 + "\n")
                f.write(f"Total files: {len(files_list)}\n")
                f.write(f"Total size: {total_size:,} bytes\n")
                f.write(f"Compressed size: {total_compressed:,} bytes\n")
                f.write(f"Overall compression: {overall_ratio:.1f}%\n")
            else:
                # Write simple format
                for filename in files_list:
                    f.write(f"{filename}\n")
                f.write(f"\nTotal files: {len(files_list)}\n")
        
        print(f"\nFile list saved to: {output_path.absolute()}")
        
    except Exception as e:
        print(f"Error saving to file: {e}")


def find_wheel_files(directory="dist"):
    """Find all wheel files in a directory."""
    wheel_dir = Path(directory)
    if not wheel_dir.exists():
        return []
    
    return list(wheel_dir.glob("*.whl"))


def main():
    parser = argparse.ArgumentParser(
        description="Build wheel and list its contents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --build                    # Build wheel and list contents
  %(prog)s --wheel path/to/file.whl   # List contents of existing wheel
  %(prog)s --build --detailed         # Build wheel and show detailed info
  %(prog)s --wheel file.whl --save wheel_contents.txt  # Save list to file
        """
    )
    
    parser.add_argument("--build", action="store_true",
                        help="Build a wheel file first")
    parser.add_argument("--wheel", type=str,
                        help="Path to existing wheel file to examine")
    parser.add_argument("--detailed", action="store_true",
                        help="Show detailed file information (size, compression, etc.)")
    parser.add_argument("--save", type=str,
                        help="Save file list to specified file")
    parser.add_argument("--output-dir", type=str, default="dist",
                        help="Directory for wheel output (default: dist)")
    
    args = parser.parse_args()
    
    wheel_path = None
    
    if args.build:
        # Build the wheel
        wheel_path = build_wheel(args.output_dir)
        if not wheel_path:
            print("Failed to build wheel file.")
            return 1
    elif args.wheel:
        # Use provided wheel file
        wheel_path = Path(args.wheel)
    else:
        # Look for existing wheel files
        wheel_files = find_wheel_files(args.output_dir)
        if wheel_files:
            wheel_path = wheel_files[0]  # Use the first one found
            print(f"Found existing wheel file: {wheel_path}")
        else:
            print("No wheel file found. Use --build to create one or --wheel to specify a path.")
            return 1
    
    if wheel_path:
        # List the contents
        files_list = list_wheel_contents(wheel_path, args.detailed, args.save)
        return 0 if files_list else 1
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
