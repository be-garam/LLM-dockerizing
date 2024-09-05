from fastapi import APIRouter, HTTPException, UploadFile, File
from app.core.models import ChatInput
from app.services.chat_service import ChatService
from app.services.pdf_service import PDFService

router = APIRouter()
chat_service = ChatService()
pdf_service = PDFService()

@router.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    try:
        response = chat_service.chat(chat_input.message, chat_input.stream_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        summary = pdf_service.summarize_pdf(content)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))