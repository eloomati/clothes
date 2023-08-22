from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Zdefiniuj model bazy danych, który będzie zawierać informacje o zdjęciach, takie jak ścieżka do pliku i unikalny identyfikator.
Base = declarative_base()

class ImageData(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    file_path = Column(String, unique=True)

#Utwórz połączenie z bazą danych i utwórz sesję, aby wykonywać operacje na bazie danych.
db_path = 'sqlite:///image_database.db'
engine = create_engine(db_path)
Session = sessionmaker(bind=engine)
session = Session()