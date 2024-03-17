#!/usr/bin/python3

import subprocess
import sys

def install_module(module):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        print(f"Successfully installed {module}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {module}, skipping...")

def main():
    with open('requirements.txt', 'r') as file:
        for line in file:
            module = line.strip()
            install_module(module)

if __name__ == "__main__":
    main()

