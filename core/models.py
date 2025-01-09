from sqlalchemy import Column, String, Integer, Text
from core.database import Base

class UserModel(Base):
    __tablename__ = "users"

    sn = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(50), unique=True, nullable=False)
    pw = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)

class PostModel(Base):
    __tablename__ = "products"

    products_id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String,  unique=True, nullable=False)
    uploaded_by = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text)
    category = Column(String)