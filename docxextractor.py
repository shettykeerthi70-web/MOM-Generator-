from docx import document 

def text_extractor_docx(file_path):
    docx_file=document(file_path)
    docx_text=''.join([p.text for p in docx_file.paragraphs])
    return docx_text