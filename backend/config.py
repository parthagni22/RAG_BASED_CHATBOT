#!/usr/bin/env python3
"""
Configuration management for the RAG system using python-dotenv
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration class for the RAG system"""

    # API Keys from environment variables
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Model Settings
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Vector Database Settings
    use_pinecone: bool = os.getenv("USE_PINECONE", "false").lower() == "true"
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "aggie-courses")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

    # Document Processing
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.1"))
    max_results: int = int(os.getenv("MAX_RESULTS", "3"))

    # Application Settings
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8080"))

    # Paths
    data_dir: Path = Path(os.getenv("DATA_DIR", "Database"))
    cache_dir: Path = Path(os.getenv("CACHE_DIR", "cache"))
    log_dir: Path = Path(os.getenv("LOG_DIR", "logs"))

    def __post_init__(self):
        """Ensure directories exist"""
        for directory in [self.data_dir, self.cache_dir, self.log_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        # Set use_pinecone based on API key availability if not explicitly set
        if not os.getenv("USE_PINECONE") and self.pinecone_api_key:
            self.use_pinecone = True


class ConfigManager:
    """Manages configuration loading and validation"""

    def __init__(self):
        self.config = Config()
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # Create logs directory
            self.config.log_dir.mkdir(exist_ok=True)

            # File handler
            fh = logging.FileHandler(self.config.log_dir / "rag_system.log")
            fh.setLevel(logging.INFO)

            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # Formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            logger.addHandler(fh)
            logger.addHandler(ch)

        return logger

    def load_config(self) -> Config:
        """Load and return configuration"""
        self.logger.info("Configuration loaded successfully from environment variables")
        return self.config

    def validate_config(self) -> tuple[bool, list[str]]:
        """Validate configuration and return status with issues"""
        issues = []

        # Check required API keys
        if not self.config.gemini_api_key:
            issues.append("GEMINI_API_KEY environment variable is required")

        # Check data directory
        if not self.config.data_dir.exists():
            issues.append(f"Data directory '{self.config.data_dir}' not found")
        else:
            files = list(self.config.data_dir.glob("*.txt")) + list(
                self.config.data_dir.glob("*.pdf")
            )
            if not files:
                issues.append(f"No data files found in '{self.config.data_dir}'")

        # Validate Pinecone if enabled
        if self.config.use_pinecone:
            if not self.config.pinecone_api_key:
                issues.append("PINECONE_API_KEY required when USE_PINECONE=true")
            else:
                try:
                    from pinecone import Pinecone

                    pc = Pinecone(api_key=self.config.pinecone_api_key)
                    indexes = [idx.name for idx in pc.list_indexes()]
                    if self.config.pinecone_index_name not in indexes:
                        issues.append(
                            f"Pinecone index '{self.config.pinecone_index_name}' not found"
                        )
                except ImportError:
                    self.config.use_pinecone = False
                    self.logger.info(
                        "Pinecone not installed, using local vector storage"
                    )
                except Exception as e:
                    issues.append(f"Pinecone validation failed: {e}")

        return len(issues) == 0, issues

    def create_sample_env(self):
        """Create a sample .env file"""
        sample_env = """# Aggie Navigator Environment Configuration

# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
DEBUG=true
HOST=127.0.0.1
PORT=8080

# Vector Store Configuration
USE_PINECONE=false
PINECONE_INDEX_NAME=aggie-courses
PINECONE_ENVIRONMENT=us-east-1

# RAG System Settings
CHUNK_SIZE=800
CHUNK_OVERLAP=100
MAX_RESULTS=3
SIMILARITY_THRESHOLD=0.1

# Model Configuration
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Paths (optional)
DATA_DIR=Database
CACHE_DIR=cache
LOG_DIR=logs
"""

        env_path = Path(".env.example")
        with open(env_path, "w") as f:
            f.write(sample_env)

        self.logger.info(f"Sample environment configuration saved to {env_path}")


# Global config instance
config_manager = ConfigManager()
config = config_manager.load_config()
