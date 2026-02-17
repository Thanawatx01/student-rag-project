import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from config import settings
from src.db import init_schema

if __name__ == "__main__":
    print("Initializing TiDB schema...")
    init_schema(embedding_dim=settings.EMBEDDING_DIM)
    print("Done. Tables: students, student_chunks")
