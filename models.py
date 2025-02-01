from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    ingredients = Column(String)
    obtaining_method = Column(String)
    
    def __repr__(self):
        return f"<Item(name={self.name})>"

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    perks = Column(String)
    description = Column(String)
    
    def __repr__(self):
        return f"<Character(name={self.name})>"

def get_engine(db_url="sqlite:///items.db"):
    """
    Create a SQLAlchemy engine. When using SQLite, disable the check for thread affinity.
    """
    if db_url.startswith("sqlite"):
        return create_engine(db_url, echo=False, connect_args={"check_same_thread": False})
    else:
        return create_engine(db_url, echo=False)

def create_tables(engine):
    Base.metadata.create_all(engine)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
