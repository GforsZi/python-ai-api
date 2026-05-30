import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
router = APIRouter(prefix="/chat", tags=["Chats"])

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

class ChatRequest(BaseModel):
    message: str
    history: list[ChatCompletionMessageParam] = []

AI_MODELS = [
    "deepseek/deepseek-v4-flash:free",
    "openai/gpt-oss-120b:free"
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
                print(f"model {model} rate limited")
                time.sleep(2)
                continue
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(
        status_code=429, detail="all model are rate limited"
    )

@router.post("/")
async def chat(req: ChatRequest):
    messages = req.history + [{"role": "user", "content": req.message}]
    reply = chat_callback(messages)
    return {"reply": reply}
