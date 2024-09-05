from pydantic import BaseModel
from typing import Optional

class ChatInput(BaseModel):
    message: str
    stream_id: Optional[str] = "default"