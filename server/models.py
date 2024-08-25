from sqlalchemy import Column, Integer, String
from db import Base

class Item(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    assigned_name = Column(String, index=True)
    container_id = Column(String)
    assigned_port = Column(Integer, unique=True, nullable=False)