from database import Base, engine, SessionLocal
from models import Item

print("Creating database tables...")

Base.metadata.create_all(bind=engine)   # Create the tables in the database

