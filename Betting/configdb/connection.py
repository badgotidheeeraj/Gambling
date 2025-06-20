from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///set.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Session=sessionmaker(bind=engine)

session=Session()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
