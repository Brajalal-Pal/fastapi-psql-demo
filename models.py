from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    on_offer = Column(Boolean, default=False)

    def __repr__(self):
        return f"Item(name={self.name}, description={self.description}, price={self.price}, on_offer={self.on_offer})"
    

# create user class
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email}, password={self.password})"
