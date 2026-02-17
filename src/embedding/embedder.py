import sys
from pathlib import Path
from typing import List, Union

_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config import settings

# Ollama embeddings
try:
    from ollama import Client
    _OLLAMA_AVAILABLE = True
except ImportError:
    _OLLAMA_AVAILABLE = False


def get_embedder():
    return OllamaEmbedder(
        base_url=settings.OLLAMA_URL,
        model=settings.OLLAMA_EMBEDDING_MODEL,
    )


class OllamaEmbedder:

    def __init__(self, base_url: str, model: str):
        self.client = Client(host=base_url) if _OLLAMA_AVAILABLE else None
        self.model = model

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        if self.client is None:
            raise RuntimeError("ollama package not installed. pip install ollama")
        if isinstance(text, str):
            text = [text]
        out = []
        for t in text:
            r = self.client.embeddings(model=self.model, prompt=t)
            out.append(r.get("embedding", []))
        return out

    @property
    def dimension(self) -> int:
        return settings.EMBEDDING_DIM
