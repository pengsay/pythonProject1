from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from f5_token import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_host}:5432/foresight"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:p785084298@127.0.0.1:3306/f5_project"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()