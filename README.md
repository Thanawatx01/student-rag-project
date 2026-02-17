# Student RAG Project

โปรเจกต์ RAG (Retrieval-Augmented Generation) สำหรับข้อมูลนักเรียน โดยใช้ embedding และฐานข้อมูล MySQL/TiDB

## โครงสร้างโปรเจกต์

```
├── config/           # การตั้งค่า
├── src/
│   ├── db/           # การเชื่อมต่อ DB และ schema
│   └── embedding/    # Embedding ด้วย Ollama
├── scripts/          # สคริปต์สำหรับ init DB และ ingest ข้อมูล
└── requirements.txt
```

## ความต้องการ

- Python 3.x
- MySQL หรือ TiDB Cloud
- Ollama (สำหรับ embedding model เช่น `nomic-embed-text`)

## การติดตั้ง

```bash
# สร้าง virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

## การตั้งค่า

1. สร้างไฟล์ `.env` ในโฟลเดอร์รากโปรเจกต์
2. ตั้งค่าตัวแปรต่อไปนี้:

| ตัวแปร | คำอธิบาย |
|--------|----------|
| `DB_HOST` | โฮสต์ MySQL/TiDB |
| `DB_PORT` | พอร์ต (เช่น 4000 สำหรับ TiDB Cloud) |
| `DB_USER` | Username |
| `DB_PASSWORD` | รหัสผ่าน |
| `DB_NAME` | ชื่อฐานข้อมูล |
| `OLLAMA_URL` | URL ของ Ollama (เช่น http://localhost:11434) |
| `OLLAMA_EMBEDDING_MODEL` | ชื่อ embedding model (เช่น nomic-embed-text) |
| `EMBEDDING_DIM` | มิติของ vector (เช่น 1024) |

## การใช้งาน

### 1. สร้าง Schema และตาราง

```bash
python scripts/int_db.py
```

สร้างตาราง `students` และ `student_chunks` (รองรับคอลัมน์ VECTOR ของ TiDB หรือใช้ `embedding_json` เป็น fallback)

### 2. Ingest ข้อมูลนักเรียน

แก้ไขข้อมูลใน `scripts/ingrest_students.py` (หรือโหลดจาก CSV) แล้วรัน:

```bash
python scripts/ingrest_students.py
```

### 3. รัน Ollama (สำหรับ embedding)

```bash
ollama run nomic-embed-text
```

## เทคโนโลยีที่ใช้

- **MySQL Connector** – เชื่อมต่อฐานข้อมูล
- **Ollama** – สร้าง embedding
- **Sentence Transformers** – รองรับการแปลงข้อความ
- **FastAPI + Uvicorn** – API server

## License

MIT
