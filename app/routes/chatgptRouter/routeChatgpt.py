from fastapi import APIRouter
from ...controller.chatgtController import chat_gpt_asker

router = APIRouter()

@router.post('/ask_gpt')
def ask_gpt(req:dict):
    return chat_gpt_asker(req)