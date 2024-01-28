import PyPDF2


def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        return "".join(reader.pages[page].extract_text() for page in range(len(reader.pages)))
