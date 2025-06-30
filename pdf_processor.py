import PyPDF2
from typing import List, Optional
from config import Config
import os

class PDFProcessor:
    def __init__(self, pdf_path: Optional[str] = None):
        self.pdf_path = pdf_path or Config.PDF_FILE_PATH
        self._content = None
    
    def extract_text(self) -> str:
        """Extract text from the PDF file"""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        
        if self._content is None:
            self._content = self._read_pdf()
        
        return self._content
    
    def _read_pdf(self) -> str:
        """Read and extract text from PDF"""
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
                    text += "\n"
                
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        
        return text.strip()
    
    def get_page_content(self, page_number: int) -> Optional[str]:
        """Get content from a specific page"""
        if not os.path.exists(self.pdf_path):
            return None
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if 0 <= page_number < len(pdf_reader.pages):
                    page = pdf_reader.pages[page_number]
                    return page.extract_text()
                else:
                    return None
                    
        except Exception as e:
            print(f"Error reading page {page_number}: {str(e)}")
            return None
    
    def get_total_pages(self) -> int:
        """Get the total number of pages in the PDF"""
        if not os.path.exists(self.pdf_path):
            return 0
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            print(f"Error getting page count: {str(e)}")
            return 0 