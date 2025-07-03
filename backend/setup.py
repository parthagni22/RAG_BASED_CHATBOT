#!/usr/bin/env python3
"""
Complete setup script for the RAG system
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import List, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class SetupManager:
    """Manages the complete setup process"""

    def __init__(self):
        self.project_root = Path.cwd()
        self.data_dir = self.project_root / "Data"
        self.keys_file = self.data_dir / "keys.txt"
        self.database_dir = self.project_root / "Database"

    def run_setup(self):
        """Run the complete setup process"""
        logger.info("🚀 Starting RAG System Setup")
        logger.info("=" * 50)

        try:
            # Step 1: Check Python version
            self.check_python_version()

            # Step 2: Install dependencies
            self.install_dependencies()

            # Step 3: Setup directories
            self.setup_directories()

            # Step 4: Setup API keys
            self.setup_api_keys()

            # Step 5: Create sample data if needed
            self.setup_sample_data()

            # Step 6: Validate configuration
            self.validate_setup()

            # Step 7: Initialize system
            self.initialize_system()

            logger.info("\n" + "=" * 50)
            logger.info("🎉 Setup completed successfully!")
            logger.info("To start the application, run: python app.py")

        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            sys.exit(1)

    def check_python_version(self):
        """Check if Python version is compatible"""
        logger.info("🐍 Checking Python version...")

        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            raise RuntimeError("Python 3.8 or higher is required")

        logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro}")

    def install_dependencies(self):
        """Install required Python packages"""
        logger.info("📦 Installing dependencies...")

        requirements = [
            "flask>=2.0.0",
            "flask-cors",
            "google-generativeai",
            "sentence-transformers",
            "scikit-learn",
            "numpy",
            "langchain",
            "langchain-community",
            "pypdf",
            "python-dotenv",
            "pinecone-client",  # Optional
        ]

        for package in requirements:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logger.info(f"✅ {package}")
            except subprocess.CalledProcessError:
                logger.warning(f"⚠️  Failed to install {package}")

    def setup_directories(self):
        """Create necessary directories"""
        logger.info("📁 Setting up directories...")

        directories = [
            self.data_dir,
            self.database_dir,
            self.project_root / "logs",
            self.project_root / "cache",
            self.project_root / "templates"
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True)
            logger.info(f"✅ {directory}")

    def setup_api_keys(self):
        """Setup API keys interactively"""
        logger.info("🔑 Setting up API keys...")

        if self.keys_file.exists():
            try:
                with open(self.keys_file, 'r') as f:
                    existing_keys = json.load(f)

                # Check if keys are already configured
                if (existing_keys.get("gemini", "") and
                    existing_keys.get("gemini") != "your_gemini_api_key_here"):
                    logger.info("✅ API keys already configured")
                    return
            except:
                pass

        logger.info("\n📝 API Key Setup Required")
        logger.info("-" * 30)

        # Gemini API key (required)
        print("\n1. Gemini API Key (REQUIRED - FREE)")
        print("   Get it from: https://aistudio.google.com/app/apikey")
        gemini_key = input("   Enter your Gemini API key: ").strip()

        if not gemini_key:
            raise ValueError("Gemini API key is required")

        # Pinecone API key (optional)
        print("\n2. Pinecone API Key (OPTIONAL)")
        print("   Get it from: https://www.pinecone.io/")
        print("   Leave blank to use local vector storage")
        pinecone_key = input("   Enter your Pinecone API key (or press Enter): ").strip()

        # OpenAI API key (optional)
        print("\n3. OpenAI API Key (OPTIONAL - for better embeddings)")
        print("   Get it from: https://platform.openai.com/api-keys")
        print("   Leave blank to use free HuggingFace embeddings")
        openai_key = input("   Enter your OpenAI API key (or press Enter): ").strip()

        # Save keys
        keys_data = {
            "gemini": gemini_key,
            "pinecone": pinecone_key or "",
            "openai": openai_key or ""
        }

        with open(self.keys_file, "w") as f:
            json.dump(keys_data, f, indent=2)

        logger.info("✅ API keys saved")

    def setup_sample_data(self):
        """Create sample data if Database is empty"""
        logger.info("📚 Checking sample data...")

        existing_files = list(self.database_dir.glob("*.txt")) + list(self.database_dir.glob("*.pdf"))

        if existing_files:
            logger.info(f"✅ Found {len(existing_files)} existing data files")
            return

        logger.info("Creating sample academic data...")
        self.create_sample_data()
        logger.info("✅ Sample data created")

    def create_sample_data(self):
        """Create sample course data"""
        sample_courses = [
            {
                "filename": "csce_629_algorithms.txt",
                "content": """CSCE 629 - Analysis of Algorithms (3 credit hours)

Prerequisites: CSCE 221 (Data Structures & Algorithms) and CSCE 222 (Discrete Structures)

Course Description:
Advanced study of algorithms and their analysis. Topics include asymptotic analysis,
divide-and-conquer algorithms, dynamic programming, greedy algorithms, graph algorithms,
network flows, linear programming, NP-completeness, and approximation algorithms.

Learning Objectives:
- Analyze the time and space complexity of algorithms
- Design efficient algorithms for computational problems
- Understand advanced algorithmic techniques
- Apply mathematical tools for algorithm analysis

Grading:
- Homework: 30%
- Midterm Exam: 30%
- Final Exam: 40%

Textbook: "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein"""
            },
            {
                "filename": "csce_636_deep_learning.txt",
                "content": """CSCE 636 - Deep Learning (3 credit hours)

Prerequisites: CSCE 633 (Machine Learning) or equivalent, Linear Algebra, Calculus

Course Description:
Introduction to deep learning methods and applications. Topics include neural networks,
convolutional neural networks, recurrent neural networks, autoencoders, generative
adversarial networks, and transformer architectures.

Learning Objectives:
- Understand fundamental concepts of deep learning
- Implement neural networks from scratch
- Apply deep learning to computer vision and NLP tasks
- Use popular deep learning frameworks (PyTorch, TensorFlow)

Projects:
- Image classification using CNNs
- Sentiment analysis with RNNs
- Final project on chosen topic

Grading:
- Projects: 50%
- Midterm: 20%
- Final: 30%"""
            },
            {
                "filename": "ms_degree_requirements.txt",
                "content": """Master of Science in Computer Science and Engineering

Degree Requirements:

Thesis Option (32 credit hours):
- Core courses: 12 credit hours
- Elective courses: 14 credit hours
- Thesis: 6 credit hours (CSCE 691)

Non-Thesis Option (36 credit hours):
- Core courses: 12 credit hours
- Elective courses: 21 credit hours
- Project: 3 credit hours (CSCE 689)

Core Course Requirements:
Students must take courses from at least 3 of the following areas:
1. Algorithms and Theory
2. Computer Systems
3. Software Engineering
4. Artificial Intelligence/Machine Learning
5. Computer Graphics/Visualization
6. Computer Networks

Research Areas:
- Artificial Intelligence and Machine Learning
- Computer Systems and Architecture
- Cybersecurity
- Data Science and Analytics
- Human-Computer Interaction
- Software Engineering

Admission Requirements:
- Bachelor's degree in Computer Science or related field
- GPA: 3.0 or higher
- GRE scores (recommended)
- Letters of recommendation"""
            }
        ]

        for course in sample_courses:
            file_path = self.database_dir / course["filename"]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(course["content"])

    def validate_setup(self):
        """Validate the setup configuration"""
        logger.info("🔍 Validating setup...")

        try:
            from config import config_manager
            is_valid, issues = config_manager.validate_config()

            if not is_valid:
                logger.error("Configuration validation failed:")
                for issue in issues:
                    logger.error(f"  - {issue}")
                raise RuntimeError("Invalid configuration")

            logger.info("✅ Configuration valid")

        except ImportError as e:
            logger.error(f"Failed to import configuration: {e}")
            raise

    def initialize_system(self):
        """Initialize and test the RAG system"""
        logger.info("🔄 Initializing RAG system...")

        try:
            from rag_system import RAGSystem

            rag = RAGSystem()
            rag.index_documents()

            # Test query
            test_response = rag.query("What courses are available?")
            if test_response:
                logger.info("✅ System initialization successful")
            else:
                logger.warning("⚠️  System initialized but test query failed")

        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            raise


def main():
    """Main setup function"""
    setup_manager = SetupManager()
    setup_manager.run_setup()


if __name__ == "__main__":
    main()