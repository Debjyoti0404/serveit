from fastapi import FastAPI
import script

app = FastAPI()


@app.post("/create")
async def create(q: str):
    if q:
        ans = script.deploy(q)
        return {"output": ans[0],
                "msg": ans[1],
                "url": ans[2]
                }
    else:
        return {"message": "default"}

@app.get("/status")
async def status():
    return {"msg": "active"}
