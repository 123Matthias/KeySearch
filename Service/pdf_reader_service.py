import PyPDF2
from pathlib import Path

class PDFReader:
    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        
    def read_all_pages(self):
        """Liest alle Seiten des PDFs"""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF nicht gefunden: {self.pdf_path}")
            
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                full_text += f"\n--- Seite {i+1} ---\n{page_text}"
                
            return full_text
    
    def read_page(self, page_number):
        """Liest eine bestimmte Seite"""
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if page_number < 1 or page_number > len(reader.pages):
                raise ValueError(f"Seite {page_number} existiert nicht")
            
            page = reader.pages[page_number - 1]
            return page.extract_text()
    
    def get_page_count(self):
        """Gibt Anzahl der Seiten zurück"""
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)



