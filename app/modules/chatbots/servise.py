from sqlalchemy.orm import Session

from app.modules.chatbots.models import Conversation, Message, RoleEnum
from app.modules.chatbots.schemas import ConversationCreate, MessageSend


def create_conversation(db: Session, data: ConversationCreate) -> Conversation:
    conv = Conversation(
        user_id=data.user_id,
        title=data.title,
        system_prompt=data.system_prompt
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)

def get_conversation(db: Session, conversation_id: int) -> Conversation | None:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def list_conversation(db: Session, user_id: int) -> list[Conversation]:
    return db.query(Conversation).filter(Conversation.user_id == user_id).all()

def delete_conversation(db: Session, conversation_id: int) -> bool:
    conv = get_conversation(db, conversation_id)
    if not conv:
        return False
    db.delete(conv)
    db.commit()
    return True

async def send_message(db: Session, conversation_id: int, data: MessageSend):
    conv = get_conversation(db, conversation_id)
    if not conv:
        raise ValueError("Conversation not found")

    user_msg = Message(conversation_id=conv.id, role=RoleEnum.user, content=data.content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    history = []
    if conv.system_prompt:
        history.append({"role": "system", "content": conv.system_prompt})

    for msq in conv.messages:
        history.append({"role": msq.role.value, "content": msq.content})

