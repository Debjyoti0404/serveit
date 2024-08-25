from fastapi import FastAPI
from db import engine, database
from contextlib import asynccontextmanager
from models import Base
import script

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.connect()
    yield
    database.disconnect()

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/create")
async def create(image_name: str, port_to_listen: int, subdomain_name: str):
    if image_name and port_to_listen and subdomain_name:
        ans = script.deploy(image_name, port_to_listen, subdomain_name)
        return {"image_name": ans[0],
                "url": ans[1],
        }
    else:
        return {"message": "default"}
    
@app.delete("/del")
async def delete(subdomain_name: str):
    if subdomain_name:
        ans = script.delete(subdomain_name)
        if ans:
            return {"msg": ans}
        else:
            return {"msg": "failed"}
    else:
        return {"msg": "failed"}

@app.get("/status")
async def status(subdomain_name: str):
    return {"msg": "active"}
