from fastapi import FastAPI

app = FastAPI()


@app.post("/create")
async def root():
    return {"message": "success"}

@app.get("/status")
async def hola():
    return {"msg": "active"}
