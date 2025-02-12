# #code for building a streamlit python app where I can drag and drop one or more pdf files that 
# will be uploaded to the server where the streamlit python app is hosted. Further the streamlit app 
# should then invoke/launch a python program that can then process this pdf file which would 
# convert the pdf file(s) to html files and then save the HTML files to a local disk. 
# Once the HTML files have been generated/converted from the pdf files, the streamlit python app should 
# provide/return a hyperlink to the end user who can then click the hyperlink to launch the html files 
# in a new browser. Alternately, the html files along with the associated javascript and images can be 
# returned for the user to download it to their local desktop/machine
# additional error handling and security measures into the above code if this is hosted on a native AWS Linux EC2 Instance?

# run the code on your local MacBook desktop. However, consider the following:
# Changes and Considerations:

# 1. Install required dependencies:
#     - pdf2htmlEX: Install using Homebrew (brew install pdf2htmlEX) or download from the official repository.
#     - PyPDF2: Install using pip (pip install PyPDF2).
#     - pymupdf (fitz): Install using pip (pip install pymupdf).
# 2. Update file paths:
#     - Change UPLOAD_DIR to a suitable local directory (e.g., ~/uploads).
# 3. Security considerations:
#     - Be cautious when running the code, as it allows file uploads and execution.
#     - Ensure you understand the implications of running the code on your local machine.
# 4. Logging:
#     - Logging will write to a file named app.log in the current working directory.


# Additional MacBook-specific considerations:

# 1. pdf2htmlEX installation:
#     - If you encounter issues installing pdf2htmlEX via Homebrew, try downloading the binary from the official repository.
# 2. Permission issues:
#     - Ensure you have write permissions to the UPLOAD_DIR and log file locations.


# Code modifications for local development:

# 1. Update UPLOAD_DIR to ~/uploads or a desired local directory.
# 2. Comment out or remove IAM role and EC2-specific configurations.


# Running the code:

# 1. Save the code in a file (e.g., app.py).
# 2. Open a terminal and navigate to the directory containing the file.
# 3. Run the code using streamlit run app.py.


# Troubleshooting:

# 1. Verify dependencies are installed correctly.
# 2. Check file permissions and paths.
# 3. Consult the Streamlit documentation and logs for errors.


# By following these steps and considerations, you should be able to run the code successfully 
# on your local MacBook desktop.



import streamlit as st
import pandas as pd
from streamlit.components.v1 import iframe
import os
import subprocess
import logging
from PIL import Image
# from PyPDF2 import PdfFileReader
import pdfplumber
import fitz  # Install using pip install pymupdf
import shutil
import webbrowser
import zipfile
import tempfile
import uuid


# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)


# Set up directory for uploaded files
UPLOAD_DIR = "/Users/Manju/Work/BoilerPlateCodeGitLocal/file_uploads"


# Function to convert PDF to HTML using pdf2htmlEX
# def convert_pdf_to_html(pdf_file_path):
#     try:
#         html_file_path = pdf_file_path.replace(".pdf", ".html")
#         subprocess.run(["pdf2htmlEX", "--zoom", "1.5", pdf_file_path, html_file_path], check=True)
#         return html_file_path
#     except subprocess.CalledProcessError as e:
#         logging.error(f"PDF conversion failed: {e}")
#         st.error("PDF conversion failed. Please check the log for details.")
def convert_pdf_to_html(pdf_file_path):
    html_file_path = pdf_file_path.replace(".pdf", ".html")
    with pdfplumber.open(pdf_file_path) as pdf:
        html = ""
        for page in pdf.pages:
            html += page.to_html()
    with open(html_file_path, "w") as f:
        f.write(html)
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
        # Generate unique filename to prevent overwriting
        #filename = f"{uuid.uuid4()}{os.path.splitext(file.name)}"
        filename=file.name
        print(f"Filename is {filename}")
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(file.read())
        print(f"Filepath is {file_path}")
        # Validate PDF file
        try:
            PdfFileReader(open(file_path, "rb"))
        except Exception as e:
            logging.error(f"Invalid PDF file: {e}")
            st.error("Invalid PDF file. Please upload a valid PDF.")

        # Convert PDF to HTML
        html_file_path = convert_pdf_to_html(file_path)

        if html_file_path:
            # Display link to HTML file
            st.markdown(f"### [{file.name} (HTML)]({html_file_path})")

            # Option to download HTML file
            with open(html_file_path, "r") as f:
                html_content = f.read()
            st.download_button("Download HTML", html_content, file_name=os.path.basename(html_file_path), mime="text/html")


# Cleanup (optional)
if st.button("Clean up"):
    try:
        shutil.rmtree(UPLOAD_DIR)
    except Exception as e:
        logging.error(f"Cleanup failed: {e}")
        st.error("Cleanup failed. Please check the log for details.")


# Additional Security Measures:

# 1. Restrict file upload size
# 2. Validate file type and content
# 3. Use temporary files instead of storing uploads
# 4. Limit concurrent uploads
# 5. Monitor logs for suspicious activity


# Consider implementing:

# 1. Authentication and authorization
# 2. Encryption for uploaded files
# 3. Regular security updates and patches
# 4. Network isolation and firewall configuration


# Additional Security Measures:

# 1. File Upload Size Restriction: Streamlit doesn't support file size restrictions. Consider using alternative libraries or frameworks.
# 2. File Type and Content Validation: Implemented basic PDF validation using PyPDF2.
# 3. Temporary Files: Used /tmp/uploads for temporary file storage.
# 4. Concurrent Upload Limitation: Streamlit doesn't support concurrent upload limits. Consider using alternative libraries or frameworks.
# 5. Log Monitoring: Logging implemented using Python's built-in logging module.

# run the code on your local MacBook desktop. However, consider the following:


# Changes and Considerations:

# 1. Install required dependencies:
#     - pdf2htmlEX: Install using Homebrew (brew install pdf2htmlEX) or download from the official repository.
#     - PyPDF2: Install using pip (pip install PyPDF2).
#     - pymupdf (fitz): Install using pip (pip install pymupdf).
# 2. Update file paths:
#     - Change UPLOAD_DIR to a suitable local directory (e.g., ~/uploads).
# 3. Security considerations:
#     - Be cautious when running the code, as it allows file uploads and execution.
#     - Ensure you understand the implications of running the code on your local machine.
# 4. Logging:
#     - Logging will write to a file named app.log in the current working directory.


# Additional MacBook-specific considerations:

# 1. pdf2htmlEX installation:
#     - If you encounter issues installing pdf2htmlEX via Homebrew, try downloading the binary from the official repository.
# 2. Permission issues:
#     - Ensure you have write permissions to the UPLOAD_DIR and log file locations.


# Code modifications for local development:

# 1. Update UPLOAD_DIR to ~/uploads or a desired local directory.
# 2. Comment out or remove IAM role and EC2-specific configurations.


# Running the code:

# 1. Save the code in a file (e.g., app.py).
# 2. Open a terminal and navigate to the directory containing the file.
# 3. Run the code using streamlit run app.py.


# Troubleshooting:

# 1. Verify dependencies are installed correctly.
# 2. Check file permissions and paths.
# 3. Consult the Streamlit documentation and logs for errors.


# By following these steps and considerations, you should be able to run the code successfully 
# on your local MacBook desktop.




