from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.chatbots.models import Conversation, Message, RoleEnum
from app.modules.chatbots.schemas import ConversationCreate

class ChatService:
    def __init__(self, ai_client):
        self.ai_client = ai_client

    async def get_response(self, message: str) -> str:
        if not message.strip():
            raise ValueError("Messages cannot be empty")

        response = await self.ai_client.chat(message)
        return response

async def create_conversation(db: AsyncSession, data: ConversationCreate):
    conv = Conversation(
        user_id=data.user_id,
        title=data.title,
        system_prompt=data.system_prompt
    )
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv

async def get_conversation_by_id_and_user(db: AsyncSession, conversation_id: int, user_id: int):
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def get_messages_by_conversation(db: AsyncSession, conversation_id: int, user_id: int):
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def add_message_to_conversation(db: AsyncSession, conversation_id: int, role: RoleEnum, content: str, created_at: datetime | None = None) -> Message:
    msg = Message(conversation_id=conversation_id, role=role, content=content, created_at=created_at or datetime.utcnow())
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def delete_message_in_conversation(db: AsyncSession, message_id: int, conversation_id: int) -> bool:
    result = await db.execute(
        select(Message).filter(Message.id == message_id, Message.conversation_id == conversation_id)
    )
    message = result.scalar_one_or_none()
    if not message:
        return False
    await db.delete(message)
    await db.commit()
    return True

async def delete_conversation_by_id_and_user(db: AsyncSession, conversation_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
    )
    conv = result.scalar_one_or_none()
    if not conv:
        return False
    await db.delete(conv)
    await db.commit()
    return True

async def list_conversation(db: AsyncSession, user_id: int) -> list[Conversation]:
    result = await db.execute(select(Conversation).filter(Conversation.user_id == user_id))
    return result.scalars().all()

