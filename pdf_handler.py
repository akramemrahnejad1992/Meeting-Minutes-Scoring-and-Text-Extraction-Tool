import requests
import os
import fitz
import pytesseract
import numpy as np
import cv2
from PIL import Image
from PyPDF2 import PdfReader
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path as necessary

def download_pdf(url: str, filename: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)

        if os.path.getsize(filename) < 1024:
            print("Warning: The downloaded PDF file is too small.")
            return False
        print(f"PDF downloaded and saved as {filename}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        return False

def extract_text_pypdf2(filename: str) -> str:
    with open(filename, 'rb') as f:
        pdf = PdfReader(f)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_pymupdf(filename: str) -> str:
    doc = fitz.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_ocr_from_images(pdf_document) -> str:
    text = ""
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_np = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            text += pytesseract.image_to_string(pil_image) + "\n"
    return text
