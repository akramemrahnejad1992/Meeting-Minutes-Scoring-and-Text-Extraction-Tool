from crawler import crawl_links, get_links, get_page_links, navigation
from pdf_handler import download_pdf, extract_text_pypdf2, extract_text_pymupdf, extract_text_ocr_from_images
from scoring import score_meeting_minutes
import os
import random
import time
import fitz
import csv

def run_scraper(url, main_url):
    pages_links = []

    #view_more_links = crawl_links(url, 'ui-read-more')
    #additional_links = crawl_links(url, 'ui-article-title', 'h1', main_url)
    #pages_links += additional_links
    view_more_links = ['https://www.farmersville.k12.ca.us/site/default.aspx?PageType=14&DomainID=483&PageID=362&ModuleInstanceID=2506&ViewID=9d7780dc-000e-458b-ba39-cfc84059b040&IsMoreExpandedView=True']
    pages_links += navigation(view_more_links, main_url)

    return pages_links

if __name__ == "__main__":
    url = 'https://www.farmersville.k12.ca.us/domain/483'
    main_url = 'https://www.farmersville.k12.ca.us'
    temp_file_path = 'temps'
    if not os.path.exists(temp_file_path):
        os.mkdir(temp_file_path)
    
    results = []
    pages_links = run_scraper(url, main_url)
    for link in pages_links:
        filename = f"{temp_file_path}/board_meeting{random.randint(0, 10000)}.pdf"
        print('Link:', link)
        if 'drive.google.com' in link:
            url_id = link.split('file/d/')[1].split('/view')[0]
            link = f"https://drive.google.com/uc?id={url_id}"
        try:
            download_pdf(link, filename)
            
            text_content = ""
            
            # Attempt to extract text using PyPDF2
            text_pypdf2 = extract_text_pypdf2(filename)
            if text_pypdf2.strip():
                print("Text extracted successfully using PyPDF2")
                text_content = text_pypdf2
            else:
                print("No text extracted using PyPDF2")
                
                # Attempt to extract text using PyMuPDF only if PyPDF2 failed
                text_pymupdf = extract_text_pymupdf(filename)
                if text_pymupdf.strip():
                    print("Text extracted successfully using PyMuPDF")
                    text_content = text_pymupdf
                else:
                    print("No text extracted using PyMuPDF")
                    
                    # If both methods fail, use OCR on images
                    print("Both text extraction methods failed. Attempting OCR on images.")
                    pdf_document = fitz.open(filename)
                    text_ocr = extract_text_ocr_from_images(pdf_document)
                    if text_ocr.strip():
                        print("Text extracted successfully using OCR")
                        text_content = text_ocr
                    else:
                        print("Failed to extract text using OCR")
        
            # Score the extracted text if any text was found
            if text_content.strip():
                score, reasons = score_meeting_minutes(text_content)
                if score and score >= 70:
                    results.append({
                        "Root URL": main_url,
                        "Document Path URL": link,
                        "Document Score": score
                    })
                    
                print(f"URL: {url}")
                print(f"Score: {score}")
                print("Reasons:")
                for reason in reasons:
                    print(f"- {reason}")
        
            # Attempt to remove the PDF file
            try:
                if os.path.exists(filename):
                    time.sleep(1)  # Optional delay
                    os.remove(filename)
                    print(f"Temporary file {filename} removed")
            except PermissionError as e:
                print(f"Failed to remove {filename}: {e}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

    # Write results to CSV file
    csv_file = 'document_score.csv'
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Root URL", "Document Path URL", "Document Score"])

        # Write header only if the file is empty
        if file.tell() == 0:
            writer.writeheader()
        
        # Write the results
        writer.writerows(results)

    print(f"Results written to {csv_file}")

