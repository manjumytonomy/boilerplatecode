#code for building a streamlit python app where I can drag and drop one or more pdf files that 
# will be uploaded to the server where the streamlit python app is hosted. Further the streamlit app 
# should then invoke/launch a python program that can then process this pdf file which would 
# convert the pdf file(s) to html files and then save the HTML files to a local disk. 
# Once the HTML files have been generated/converted from the pdf files, the streamlit python app should 
# provide/return a hyperlink to the end user who can then click the hyperlink to launch the html files 
# in a new browser. Alternately, the html files along with the associated javascript and images can be 
# returned for the user to download it to their local desktop/machine
import streamlit as st
import pandas as pd
from streamlit.components.v1 import iframe
import os
import subprocess
from PIL import Image
from PyPDF2 import PdfFileReader
import fitz  # Install using pip install pymupdf
import shutil
import webbrowser
import zipfile


# Set up directory for uploaded files
UPLOAD_DIR = "uploads"


# Function to convert PDF to HTML using pdf2htmlEX
def convert_pdf_to_html(pdf_file_path):
    html_file_path = pdf_file_path.replace(".pdf", ".html")
    subprocess.run(["pdf2htmlEX", "--zoom", "1.5", pdf_file_path, html_file_path])
    return html_file_path


# Streamlit app
st.title("PDF to HTML Converter")


# File uploader with drag-and-drop support
uploaded_files = st.file_uploader("Select PDF files", type=["pdf"], accept_multiple_files=True)


# Process uploaded files
if uploaded_files:
    # Create upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Save uploaded files to upload directory
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

        # Convert PDF to HTML
        html_file_path = convert_pdf_to_html(file_path)

        # Display link to HTML file
        st.markdown(f"### [{file.name} (HTML)]({html_file_path})")

        # Option to download HTML file
        with open(html_file_path, "r") as f:
            html_content = f.read()
        st.download_button("Download HTML", html_content, file_name=os.path.basename(html_file_path), mime="text/html")


# Optional: Display uploaded PDF file
st.markdown("### Uploaded PDF")
if uploaded_files:
    pdf_file = uploaded_files[0]
    with open(os.path.join(UPLOAD_DIR, pdf_file.name), "rb") as f:
        pdf_content = f.read()
    st.components.v1.iframe(src=pdf_content, width="100%", height=600)


# Cleanup (optional)
#if st.button("Clean up"):
#    shutil.rmtree(UPLOAD_DIR)


# Prerequisites:

# 1. Install required libraries using pip:

# ```
# pip install streamlit PyPDF2 pymupdf

# 2. Install pdf2htmlEX using your package manager or from the official repository:
#    - Ubuntu/Debian: sudo apt-get install pdf2htmlEX
#    - macOS (with Homebrew): brew install pdf2htmlEX
#    - Windows: Download from [here](https://github.com/coolwanglu/pdf2htmlEX/releases)


# *Functionality:*

# 1. Drag-and-drop PDF file(s) upload.
# 2. Conversion of uploaded PDF(s) to HTML using pdf2htmlEX.
# 3. Display link to generated HTML file.
# 4. Option to download HTML file.
# 5. Optional display of uploaded PDF file.


# *Notes:*

# - This code uses the pdf2htmlEX command-line tool for PDF-to-HTML conversion.
# - Ensure pdf2htmlEX is installed and accessible in your system's PATH.
# - Adjust the upload directory (UPLOAD_DIR) as needed.
# - You may want to implement additional error handling and security measures depending on your deployment environment.
