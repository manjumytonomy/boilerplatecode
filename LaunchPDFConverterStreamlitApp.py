#Streamlit app code to launch the WEPackageGenerator shell script embedded within the streamlit app

import streamlit as st
import subprocess
import threading
import configparser
import logging

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Set up logging
logging.basicConfig(level=config['LOGGING']['log_level'])

# Function to run shell script
def run_shell_script(script_path, step_name):
    # Call your existing function
    subprocess.run(['bash', script_path])

# Streamlit app
st.title("Launch Script")
st.write("Click the button to launch the script")

# Button to launch script
if st.button("Launch Script"):
    # Get script paths and names from config
    scripts = {
        'setup.sh': 'Install Dependencies',
        'PDFDownloader/run_PDFDownloader.sh': 'Download files',
        'QR URL Check/run_QRURLChecker.sh': 'QR and URL Checker',
        'PDFToHtmlConverter/run_MytonomyPDFConverter.sh': 'Convert Files',
        'Tag Insertion/run_MetaTagGenerator.sh': 'Insert tags and renamed',
        'EpicDesktop/run_EpicDesktopIndex.sh': 'Create EpicDesktopIndex',
        '../Code Unit Test/run_unittest.sh': 'Run Unit Test',
        'Tag Validator/run_epic_tag_validator.sh': 'Run Validator',
        'Dropbox Uploader/run_dropboxUploader.sh': 'Run Uploader'
    }

    # Run scripts based on configuration
    for script_path, step_name in scripts.items():
        if config['OPTION_FLAGS'].getboolean(step_name.replace(' ', '').lower()):
            threading.Thread(target=run_shell_script, args=(script_path, step_name)).start()
            logging.info(f"Launched {step_name}")
            st.write(f"Launched {step_name}")
``


#To integrate this with your existing code:


#1.  Move your `run_shell_script` function to a separate file (e.g., `utils.py`) to avoid duplication.
#2.  Update the `run_shell_script` function in the Streamlit app to call your existing function.
#3.  Ensure the `config.ini` file is accessible by the Streamlit app.


#Run the Streamlit app using:


#bash
#streamlit run app.py
```


#Open your web browser and navigate to http://localhost:8501 to access the Streamlit app.


#Clicking the "Launch Script" button will launch the shell scripts based on the configuration in config.ini.