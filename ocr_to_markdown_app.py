import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract

# Configure Tesseract path if needed
pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file using Tesseract OCR.

    Args:
        pdf_file: The uploaded PDF file.

    Returns:
        dict: A dictionary mapping page numbers to extracted text.
    """
    ocr_results = {}

    # Convert PDF pages to images
    images = convert_from_bytes(pdf_file.read())

    for page_number, image in enumerate(images, start=1):
        # Perform OCR on the image
        text = pytesseract.image_to_string(image)
        ocr_results[page_number] = text or "No text found on this page."

    return ocr_results

# Streamlit App
st.title("PDF to Text Extractor (Local OCR)")
st.write("Upload a PDF file to extract text using Tesseract OCR.")

# File Uploader
uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf:
    with st.spinner("Processing the PDF..."):
        try:
            ocr_results = extract_text_from_pdf(uploaded_pdf)
            st.success("OCR completed!")

            # Display the results
            for page_number, text in ocr_results.items():
                st.write(f"### Page {page_number}")
                st.text_area(f"Extracted Text (Page {page_number})", text, height=200)

            # Option to download the results
            all_text = "\n".join([f"--- Page {page} ---\n{text}" for page, text in ocr_results.items()])
            st.download_button("Download Extracted Text", data=all_text, file_name="extracted_text.txt", mime="text/plain")
        except Exception as e:
            st.error(f"An error occurred: {e}")
