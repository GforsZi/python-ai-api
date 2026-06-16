import os
import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from openai import OpenAI
from dotenv import load_dotenv

from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.modules.chatbots import schemas, service
from app.modules.chatbots.models import RoleEnum
from app.shared.utils import ApiResponse

load_dotenv()
router = APIRouter(prefix="/chat", tags=["Chats"])

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

AI_MODELS = [
    "nex-agi/nex-n2-pro:free",
    "poolside/laguna-xs.2:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
]

def chat_callback(messages: list):
    for model in AI_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                time.sleep(2)
                continue
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=429, detail="all model are rate limited")

@router.post("/new")
async def new_chat(
    data: schemas.ConversationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user())
):
    data.user_id = current_user.id
    result = await service.create_conversation(db, data)
    return ApiResponse(message="result", data=result)

@router.post("/send/{conversation_id}")
async def send_to_existing_chat(
    conversation_id: int,
    data: schemas.MessageSend,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user())
):
    conv = await service.get_conversation_by_id_and_user(db, conversation_id, current_user.id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Save user message
    await service.add_message_to_conversation(db, conversation_id, RoleEnum.user, data.content)
    
    # Prepare history
    history = []
    if conv.system_prompt:
        history.append({"role": "system", "content": conv.system_prompt})
    for m in conv.messages:
        history.append({"role": m.role.value, "content": m.content})
    history.append({"role": "user", "content": data.content})
    
    # Call AI
    reply = chat_callback(history)
    
    # Save AI response
    await service.add_message_to_conversation(db, conversation_id, RoleEnum.assistant, reply)
    
    return {"reply": reply}

@router.get("/view/{conversation_id}", response_model=schemas.ConversationOut)
async def view_chat(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user())
):
    conv = await service.get_messages_by_conversation(db, conversation_id, current_user.id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Model uses 'message' (singular) for the relationship, Schema uses 'messages'
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "created_at": conv.created_at,
        "messages": conv.messages 
    }

@router.delete("/message/{conversation_id}/{message_id}")
async def delete_message(
    conversation_id: int,
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user())
):
    if not await service.delete_message_in_conversation(db, message_id, conversation_id):
        raise HTTPException(status_code=404, detail="Message not found")
    return {"detail": "Message deleted"}

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user())
):
    if not await service.delete_conversation_by_id_and_user(db, conversation_id, current_user.id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"detail": "Conversation deleted"}

