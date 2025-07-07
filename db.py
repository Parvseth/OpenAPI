from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ PostgreSQL connection URL format (update these values)
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://your_username:your_password@localhost/your_dbname"

# ✅ PostgreSQL does NOT need `check_same_thread`
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
