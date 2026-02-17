import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config import settings
from src.db.connection import get_mysql_connection

def init_schema(embedding_dim: int = 768) -> None:
    with get_mysql_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}`")
            conn.commit()
        finally:
            conn.close()

    with get_mysql_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT PRIMARY KEY,
                    age INT NOT NULL,
                    gender VARCHAR(20) NOT NULL,
                    academic_level VARCHAR(50) NOT NULL,

                    study_hours FLOAT,
                    self_study_hours FLOAT,
                    online_classes_hours FLOAT,
                    social_media_hours FLOAT,
                    gaming_hours FLOAT,
                    sleep_hours FLOAT,
                    screen_time_hours FLOAT,

                    exercise_minutes INT,
                    caffeine_intake_mg INT,

                    part_time_job BOOLEAN,
                    upcoming_deadline BOOLEAN,

                    internet_quality VARCHAR(50),

                    mental_health_score FLOAT,
                    focus_index FLOAT,
                    burnout_level FLOAT,
                    productivity_score FLOAT,
                    exam_score FLOAT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            try:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS student_chunks (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT NOT NULL,
                        content TEXT NOT NULL COMMENT 'ข้อความที่ใช้ embed',
                        embedding VECTOR({embedding_dim}) COMMENT 'vector จาก embed model',
                        meta_json TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_student_id (student_id),
                        VECTOR INDEX idx_embedding (embedding)
                            USING HNSW
                            WITH ('distance_type' = 'cosine')
                    )
                """)
            except Exception as e:
                if "VECTOR" in str(e) or "Unknown" in str(e):
                    # Fallback ถ้า TiDB version ไม่รองรับ VECTOR
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS student_chunks (
                            id BIGINT AUTO_INCREMENT PRIMARY KEY,
                            student_id INT NOT NULL,
                            content TEXT NOT NULL,
                            embedding_json TEXT COMMENT 'embedding as JSON array',
                            meta_json TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            INDEX idx_student_id (student_id)
                        )
                    """)
                else:
                    raise

        conn.commit()
