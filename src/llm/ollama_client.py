import sys
from pathlib import Path
from typing import Iterator

_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config import settings

try:
    from ollama import Client
    _OLLAMA_AVAILABLE = True
except ImportError:
    _OLLAMA_AVAILABLE = False


class OllamaChat:

    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.client = Client(host=base_url or settings.OLLAMA_URL) if _OLLAMA_AVAILABLE else None
        self.model = model or settings.OLLAMA_MODEL

    def chat(self, messages: list[dict], stream: bool = False):
        if self.client is None:
            raise RuntimeError("ollama package not installed. pip install ollama")
        return self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream,
        )

    def ask_with_context(self, question: str, context: str) -> str:
        system = (
            "คุณเป็นผู้ช่วยตอบคำถามเกี่ยวกับข้อมูลนักเรียน "
            "ตอบจาก context ที่ให้มาเท่านั้น ถ้าไม่มีข้อมูลใน context ให้บอกว่าไม่มีข้อมูล."
        )
        user = f"Context:\n{context}\n\nQuestion: {question}"
        resp = self.chat([
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])
        return resp.get("message", {}).get("content", "")

    def ask_with_context_stream(self, question: str, context: str) -> Iterator[str]:
        system = (
            "คุณเป็นผู้ช่วยตอบคำถามเกี่ยวกับข้อมูลนักเรียน "
            "ตอบจาก context ที่ให้มาเท่านั้น ถ้าไม่มีข้อมูลใน context ให้บอกว่าไม่มีข้อมูล."
        )
        user = f"Context:\n{context}\n\nQuestion: {question}"
        stream = self.chat([
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ], stream=True)
        for chunk in stream:
            part = chunk.get("message", {}).get("content", "")
            if part:
                yield part
