import PyPDF2

def get_num_pages(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return len(pdf_reader.pages)

file_path = "MNIST Code.pdf"
print(get_num_pages(file_path))