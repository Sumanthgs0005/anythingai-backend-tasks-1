import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

TESTING = ("PYTEST_CURRENT_TEST" in os.environ) or ("pytest" in sys.modules)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:" if TESTING else "sqlite:///./tasks.db"

# Track last test id so we can reset DB once per test function
last_test_id = None

if TESTING:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
