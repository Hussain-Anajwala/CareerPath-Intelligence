"""Application configuration module."""

import os
from pathlib import Path
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


@dataclass
class Settings:
    """Application settings and paths."""
    
    APP_NAME: str = "CareerPath Intelligence"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Path Configuration
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    INTERIM_DATA_DIR: Path = DATA_DIR / "interim"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    REFERENCE_DATA_DIR: Path = DATA_DIR / "reference"
    MODELS_DIR: Path = BASE_DIR / "models"
    DOCS_DIR: Path = BASE_DIR / "docs"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/careerpath.db")
    
    # ML & Similarity Search
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.65"))
    DEFAULT_TOP_K: int = int(os.getenv("DEFAULT_TOP_K", "5"))


settings = Settings()
