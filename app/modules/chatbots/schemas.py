from datetime import datetime
from pydantic import BaseModel

from app.modules.chatbots.models import RoleEnum


class ConversationCreate(BaseModel):
    user_id: int
    title: str | None = None
    system_prompt: str | None = "You are a helpful assistant."

class MessageSend(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    role: RoleEnum
    content: str
    created_at: datetime
    
    class config:
        from_attributes = True

class ConversationOut(BaseModel):
    id: int
    user_id: int
    title: str | None
    created_at: datetime
    messages: list[MessageOut] = []

    class config:
        from_attributes = True

class ChatReply(BaseModel):
    conversation_id: int
    user_message: MessageOut
    ai_reply: MessageOut
