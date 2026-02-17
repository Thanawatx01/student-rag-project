import os
from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_env_path)

class Settings:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    SSL_CA: str = os.getenv("SSL_CA")
    SSL_VERIFY: bool = os.getenv("SSL_VERIFY")
    SSL_VERIFY_IDENTITY: bool = os.getenv("SSL_VERIFY_IDENTITY")

    @property
    def mysql_connection_dict(self) -> dict:
        return {
            "host": self.DB_HOST,
            "port": self.DB_PORT,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "database": self.DB_NAME,
            "ssl_ca": self.SSL_CA,
            "ssl_verify": self.SSL_VERIFY,
            "ssl_verify_identity": self.SSL_VERIFY_IDENTITY,
        }

    OLLAMA_URL: str = os.getenv("OLLAMA_URL")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")
    OLLAMA_EMBEDDING_MODEL: str = os.getenv("OLLAMA_EMBEDDING_MODEL")

    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "768"))

settings = Settings()