1. Create a requirements.txt File
Create a text file named requirements.txt in the same folder as your Python script and add the following content:


Pillow

Note:
Tkinter: This GUI library typically comes pre-installed with Python on macOS.
Ghostscript: This is a system dependency and must be installed via Homebrew (see below).

2. Installation Instructions
Follow these steps to set up your environment and run the PDF and Image Shrinker GUI tool:

Step 1: Install Homebrew (if not already installed)
Open Terminal and run the following command to install Homebrew:


/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Step 2: Install Ghostscript
Ghostscript is required for compressing PDF files. Once Homebrew is installed, run:

brew install ghostscript

Step 3: Install Python 3
If you haven't already installed Python 3 or wish to install the latest version via Homebrew:

brew install python

You can verify your Python version with:
python3 --version

Step 4: Set Up a Virtual Environment (Optional but Recommended)
Create a virtual environment to keep dependencies isolated:
python3 -m venv venv

Activate the virtual environment:
source venv/bin/activate

Step 5: Install Python Dependencies
Make sure your requirements.txt file is in your working directory. Then run:
pip install -r requirements.txt

This command installs the Pillow library (which is required for image compression).

Step 6: Run the Script
Assuming your script is named pdf_image_shrinker_gui.py, run the program with:
python3 pdf_image_shrinker_gui.py

A window should open with options to select input files, set the output directory, adjust compression settings, and run the file shrink operation.
