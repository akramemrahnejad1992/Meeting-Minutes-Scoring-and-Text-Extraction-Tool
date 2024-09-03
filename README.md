# Meeting Minutes Scoring and Text Extraction Tool

This project is designed to extract text from PDF documents and score meeting minutes based on predefined criteria. It utilizes Tesseract OCR for text extraction and a web crawler for scraping relevant URLs.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Directory Structure](#directory-structure)
- [Troubleshooting](#troubleshooting)
- [Output](#output)

## Setup Instructions

### Step 1: Set Up Your Environment

1. **Create a Project Directory**: Ensure you have the project structure as outlined below.

2. **Install Required Packages**: Create a `requirements.txt` file with the necessary libraries. Here’s a sample content for it:
   ```
   pytesseract
   requests
   beautifulsoup4
   pandas
   ```

3. **Install the Dependencies**: Navigate to your project directory in your terminal or command prompt and run:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Set Up Tesseract

1. **Install Tesseract**: Make sure you have Tesseract OCR installed on your machine. You can download it from [here](https://github.com/tesseract-ocr/tesseract).

2. **Set the Path**: Ensure that the path to the Tesseract executable is correctly set in your `pdf_handler.py`. For example:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path as necessary
   ```

### Step 3: Run the Project

1. **Run the Main Script**: Navigate to your project directory in your terminal or command prompt and execute:
   ```bash
   python main.py
   ```

## Directory Structure

Your project directory should look like this:

```
project/
│
├── main.py                  # Main entry point
├── crawler.py               # Contains functions for crawling links
├── pdf_handler.py           # Handles PDF downloading and text extraction
├── scoring.py               # Contains scoring logic for meeting minutes
├── requirements.txt         # List of required packages
```

## Troubleshooting

- If you encounter any issues, check the console for error messages and ensure all dependencies are correctly installed.
- If you're using a different browser, make sure to adjust the WebDriver setup accordingly.
- If the code gets stuck on a page and does not navigate to the next page, simply stop the execution and rerun the code. This may help in overcoming temporary issues with page loading or navigation.

## Output

The results will be saved in `document_scores.csv`. If the file already exists, new results will be appended.
```

### Notes:
- Feel free to modify any sections to better fit your project's specifics.
- Make sure to include any additional setup instructions or dependencies that may be necessary for your specific implementation.
=======
# Meeting-Minutes-Scoring-and-Text-Extraction-Tool
>>>>>>> 112e54d4bf534bda90a85d6e709ac5590719ddc1
