import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

@dataclass(frozen=True)
class Settings:
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", "").strip(), repr=False)
    model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-6-luna").strip())
    access_token: str = field(default_factory=lambda: os.getenv("APP_ACCESS_TOKEN", "").strip(), repr=False)
    vercel: bool = field(default_factory=lambda: os.getenv("VERCEL") == "1")
    cors_origins: tuple = field(default_factory=lambda: tuple(x.strip() for x in os.getenv("CORS_ORIGINS", "").split(",") if x.strip()))
