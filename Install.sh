#!/bin/bash

# Verify Python 3 installation
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Install it with 'pkg install python3'."
    exit 1
fi

# Verify if pip3 is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 is not installed, installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install rgbprint Python package
pip3 install rgbprint

# Test the installation by importing Python modules
python3 -c "
try:
    import rgbprint
    import requests
    import platform
    import subprocess
    import datetime
    import hashlib
    from rgbprint import gradient_print, Color
    print('All libraries (including rgbprint) installed successfully.')
except ImportError as e:
    print(f'Error importing libraries: {e}')
"

# Final installation message
echo "Installation completed successfully! 🎉"
echo "Tip: Use 'clear' to clean up the console screen. 💫"
