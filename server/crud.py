from fastapi import Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Item

async def create_item(name: str, id: str, port: int, db: Session = Depends(get_db)):
    item = Item(assigned_name=name, container_id=id, assigned_port=port)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

async def read_item(name: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.assigned_name == name).first()
    if item is None:
        return None
    return item

async def delete_item(name: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.assigned_name == name).first()
    if item is None:
        return False
    
    db.delete(item)
    db.commit()
    return True