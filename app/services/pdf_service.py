from pypdf import PdfReader
from io import BytesIO
from app.services.chat_service import ChatService

class PDFService:
    def __init__(self):
        self.chat_service = ChatService()

    def extract_text_from_pdf(self, pdf_content):
        pdf = PdfReader(BytesIO(pdf_content))
        return ' '.join(page.extract_text() for page in pdf.pages)

    def summarize_text(self, text, max_size=5000):
        summarized_text = text
        while len(summarized_text) > max_size:
            messages = [
                {"role": "system", "content": "Summarize the following text, preserving key information:"},
                {"role": "user", "content": summarized_text[:max_size]}
            ]
            summarized_text = self.chat_service.call_api(messages)
        return summarized_text

    def summarize_pdf(self, pdf_content):
        extracted_text = self.extract_text_from_pdf(pdf_content)
        return self.summarize_text(extracted_text)