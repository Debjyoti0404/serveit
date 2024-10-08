from sqlalchemy.orm import Session
from database import get_db
from models import Item

def create_item(name: str, id: str, port: int, db: Session):
    item = Item(assigned_name=name, container_id=id, assigned_port=port)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def read_item(name: str, db: Session):
    item = db.query(Item).filter(Item.assigned_name == name).first()
    if item is None:
        return None
    return item

def delete_item(name: str, db: Session):
    item = db.query(Item).filter(Item.assigned_name == name).first()
    if item is None:
        return False
    
    db.delete(item)
    db.commit()
    return True