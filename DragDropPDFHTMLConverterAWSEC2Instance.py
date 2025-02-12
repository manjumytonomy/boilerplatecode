# #code for building a streamlit python app where I can drag and drop one or more pdf files that 
# will be uploaded to the server where the streamlit python app is hosted. Further the streamlit app 
# should then invoke/launch a python program that can then process this pdf file which would 
# convert the pdf file(s) to html files and then save the HTML files to a local disk. 
# Once the HTML files have been generated/converted from the pdf files, the streamlit python app should 
# provide/return a hyperlink to the end user who can then click the hyperlink to launch the html files 
# in a new browser. Alternately, the html files along with the associated javascript and images can be 
# returned for the user to download it to their local desktop/machine
# additional error handling and security measures into the above code if this is hosted on a native AWS Linux EC2 Instance?

import streamlit as st
import pandas as pd
from streamlit.components.v1 import iframe
import os
import subprocess
import logging
from PIL import Image
from PyPDF2 import PdfFileReader
import fitz  # Install using pip install pymupdf
import shutil
import webbrowser
import zipfile
import tempfile
import uuid


# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)


# Set up directory for uploaded files
UPLOAD_DIR = "/tmp/uploads"


# Function to convert PDF to HTML using pdf2htmlEX
def convert_pdf_to_html(pdf_file_path):
    try:
        html_file_path = pdf_file_path.replace(".pdf", ".html")
        subprocess.run(["pdf2htmlEX", "--zoom", "1.5", pdf_file_path, html_file_path], check=True)
        return html_file_path
    except subprocess.CalledProcessError as e:
        logging.error(f"PDF conversion failed: {e}")
        st.error("PDF conversion failed. Please check the log for details.")


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
        filename = f"{uuid.uuid4()}{os.path.splitext(file.name)}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(file.read())

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


# Considerations for AWS Linux EC2 Instance:

# 1. Ensure the EC2 instance has the necessary dependencies installed (e.g., pdf2htmlEX).
# 2. Configure IAM roles and permissions for the EC2 instance.
# 3. Monitor EC2 instance logs and security groups.
# 4. Regularly update and patch the EC2 instance.

# step-by-step guide to run the Streamlit app on an AWS Linux EC2 instance:


# Prerequisites:

# 1. AWS account with EC2 access.
# 2. Basic knowledge of Linux commands.


# Step 1: Launch an EC2 Instance

# 1. Log in to the AWS Management Console.
# 2. Navigate to the EC2 dashboard.
# 3. Click "Launch Instance" and select:
#     - Amazon Linux 2 (or your preferred Linux distribution).
#     - Instance type (e.g., t2.micro).
#     - Configure security group to allow inbound traffic on port 8080 (or your desired port).
# 4. Launch the instance.


# Step 2: Connect to the EC2 Instance

# 1. Wait for the instance to launch.
# 2. Click "Connect" and select "SSH client" or "EC2 Instance Connect".
# 3. Use the provided SSH command or EC2 Instance Connect to access the instance.


# Step 3: Install Dependencies

# 1. Update package list: sudo yum update -y
# 2. Install Python 3.8+ (if not already installed): sudo yum install -y python3
# 3. Install pip: sudo yum install -y python3-pip
# 4. Install Streamlit: pip3 install streamlit
# 5. Install additional dependencies:
#     - pdf2htmlEX: sudo yum install -y epel-release; sudo yum install -y pdf2htmlEX
#     - PyPDF2: pip3 install PyPDF2
#     - pymupdf (fitz): pip3 install pymupdf


# Step 4: Configure the Instance

# 1. Create a new directory for your app: mkdir /home/ec2-user/app
# 2. Copy your Streamlit app code to the instance using SCP or SFTP.


# Step 5: Run the Streamlit App

# 1. Navigate to the app directory: cd /home/ec2-user/app
# 2. Run the Streamlit app: streamlit run app.py (assuming your app file is named app.py)
# 3. Access the app by visiting http://<EC2_INSTANCE_PUBLIC_IP>:8080 in your web browser.


# Step 6: Ensure Continuous Running

# 1. Use a process manager like systemd or supervisord to keep the app running.
# 2. Configure the instance to restart the app on reboot.


# Additional Security Considerations:

# 1. Secure your EC2 instance with IAM roles and permissions.
# 2. Configure security groups to restrict inbound traffic.
# 3. Monitor instance logs and security.


# Troubleshooting:

# 1. Verify dependencies are installed correctly.
# 2. Check file permissions and paths.
# 3. Consult Streamlit documentation and logs for errors.


# By following these steps, you should be able to successfully run your Streamlit app on an AWS Linux EC2 instance