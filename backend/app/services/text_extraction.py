from pypdf import PdfReader

def extract_text(file_path):
    reader=PdfReader(file_path)
    extracted_pages=[]
    for page_number, page in enumerate(reader.pages):
        text=page.extract_text()
        if text:
            extracted_pages.append({"page":page_number +1,"text":text})

    return extracted_pages