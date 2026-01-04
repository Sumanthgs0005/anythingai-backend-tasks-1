import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///./test.db"

# pytest configuration
pytest_plugins = []
