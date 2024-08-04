from fastapi import FastAPI
import script

app = FastAPI()


@app.post("/create")
async def create(q: str):
    if q:
        ans = script.deploy(q)
        return {"image_name": ans[0],
                "url": ans[1],
        }
    else:
        return {"message": "default"}

@app.get("/status")
async def status():
    return {"msg": "active"}
