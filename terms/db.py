from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from terms.config import Settings

settings = Settings()
ENGINE = create_engine(settings.DATABASE_URL, future=True)
Session = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)
