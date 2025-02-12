import os
import fitz
import pandas as pd

def main():
    #folder_path = "/Users/vikram/Work/Mytonomy/Latest/166 Carolina East PDFS 10-24-24"
    folder_path="/Users/manju/Mytonomy Inc Dropbox/Manju Komarlu/4b_CONTENT_FINAL_WE"
    #folder_path="/Users/manju/Work/WrittenEducation Project/Customer Releases/Carolina East/Carolina East 10-4-24 PDFs"
    folder = folder_path.split(os.sep)[-1]
    df = pd.DataFrame(columns=["Customer", "Logo", "Logo", "Condition Area", "Filepath", "Title", "Unique Name", "Keyword", "Diagnosis Code", "CPT Code", 
                               "Language", "Corresponding Language", "Language Index", "Source", "Document Type", "QR Code", "Short URL", "Customer Disclaimer"])
    
    filepaths = []
    titles = []
    keywords = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(dirpath, filename)
                idx = pdf_path.find(folder)
                filepaths.append(os.sep + pdf_path[idx:])

                doc = fitz.open(pdf_path)
                titles.append(doc.metadata.get('title'))
                keywords.append(doc.metadata.get('keywords'))

    df["Filepath"] = filepaths
    df["Title"] = titles
    df["Keyword"] = keywords

    df.to_excel(f'{folder}.xlsx')

if __name__ == "__main__":
    main()
