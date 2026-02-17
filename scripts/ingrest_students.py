#!/usr/bin/env python3
"""
โหลดข้อมูลนักเรียนเข้า TiDB และสร้าง embedding เก็บใน student_chunks.

ใช้ได้ทั้งตารางที่มีคอลัมน์ VECTOR(embedding) หรือ embedding_json (fallback).
ตัวอย่างข้อมูล: แก้ students_data ด้านล่างหรืออ่านจาก CSV.
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from config import settings
from src.db.connection import get_connection
from src.embedding import get_embedder

# ตัวอย่างข้อมูลนักเรียน (หรือโหลดจาก CSV)
STUDENTS_DATA = [
    {"student_id": "64001", "name": "สมชาย ใจดี", "grade": "ม.1", "room": "1/1"},
    {"student_id": "64002", "name": "สมหญิง รักเรียน", "grade": "ม.1", "room": "1/1"},
    {"student_id": "64003", "name": "วิชัย ตั้งใจ", "grade": "ม.2", "room": "2/1"},
]


def build_chunk_text(row: dict) -> str:
    """สร้างข้อความหนึ่ง chunk ต่อหนึ่งนักเรียน (สำหรับ embed)."""
    return (
        f"รหัสนักเรียน {row['student_id']} ชื่อ {row['name']} "
        f"ระดับชั้น {row.get('grade', '')} ห้อง {row.get('room', '')}"
    )


def table_has_vector_column(conn) -> bool:
    """ตรวจว่าตาราง student_chunks มีคอลัมน์ embedding (VECTOR) หรือไม่."""
    with conn.cursor() as cur:
        cur.execute("SHOW COLUMNS FROM student_chunks LIKE 'embedding'")
        return cur.fetchone() is not None


def main():
    conn_params = settings.tidb_connection_dict
    embedder = get_embedder()

    with get_connection() as conn:
        has_vector = table_has_vector_column(conn)

        for row in STUDENTS_DATA:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO students (student_id, name, grade, room, info_json)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE name=%s, grade=%s, room=%s
                    """,
                    (
                        row["student_id"],
                        row["name"],
                        row.get("grade", ""),
                        row.get("room", ""),
                        json.dumps(row, ensure_ascii=False),
                        row["name"],
                        row.get("grade", ""),
                        row.get("room", ""),
                    ),
                )

            content = build_chunk_text(row)
            vec = embedder.embed(content)[0]

            if has_vector:
                vec_str = "[" + ",".join(str(round(x, 6)) for x in vec) + "]"
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO student_chunks (student_id, content, embedding, meta_json)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (row["student_id"], content, vec_str, json.dumps(row, ensure_ascii=False)),
                    )
            else:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO student_chunks (student_id, content, embedding_json, meta_json)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            row["student_id"],
                            content,
                            json.dumps(vec),
                            json.dumps(row, ensure_ascii=False),
                        ),
                    )

    print("Ingested", len(STUDENTS_DATA), "students and chunks.")


if __name__ == "__main__":
    main()
