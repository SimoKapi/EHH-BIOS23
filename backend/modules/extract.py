import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_document, page_number, rect):
    """
    Extract text from a specific rectangular area on a PDF page.
    
    Parameters:
    - pdf_document: pdf_document = fitz.open(pdf_path)
    - page_number (int): Page number from which to extract text (1-indexed).
    - rect (tuple): Rectangular area coordinates in the format (x0, y0, x1, y1).

    Returns:
    - str: Extracted text.
    """

    # Get the specified page
    page = pdf_document[page_number - 1]

    # print(page.rect)

    # Define the rectangular area
    rect = fitz.Rect(*rect)

    # Get the text within the specified rectangular area
    # print(page.get_text("text"))
    text = page.get_text("text", clip=rect).strip()

    # Close the PDF document
    # pdf_document.close()

    return text