import os
from dotenv import load_dotenv
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "50"))
USE_GPU = os.getenv("USE_GPU", "true").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))

# Validate environment variables
if not all([HF_TOKEN, MODEL_NAME]):
    raise ValueError("Missing required environment variables: HUGGINGFACE_TOKEN or MODEL_NAME")

# GPU 사용 설정
device = "cuda" if USE_GPU and torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")

# 모델 및 토크나이저 로드 함수
def load_model_and_tokenizer():
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, 
            token=HF_TOKEN, 
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        ).to(device)
        logger.info(f"Model {MODEL_NAME} loaded successfully")
        return tokenizer, model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

tokenizer, model = load_model_and_tokenizer()

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(input_data: TextInput) -> Dict[str, Any]:
    try:
        inputs = tokenizer(input_data.text, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"generated_text": response}
    except Exception as e:
        logger.error(f"Error in text generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root() -> Dict[str, str]:
    return {
        "message": "Welcome to the Llama 3 API",
        "device": device,
        "model": MODEL_NAME,
        "max_new_tokens": MAX_NEW_TOKENS
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)