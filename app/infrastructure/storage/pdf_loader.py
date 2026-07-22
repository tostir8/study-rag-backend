import fitz


class PDFLoader:
    """
    Loads PDF documents using PyMuPDF.

    Responsible for extracting the plain text
    from every page in the document.
    """

    def load(self, pdf_path: str) -> str:
        """
        Extracts all text from a PDF file.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            Complete extracted text.
        """

        document = fitz.open(pdf_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)
