from fastapi import FastAPI

app = FastAPI()


@app.get("/startup")
def startup():
    return True


@app.get("/livez")
def liveness():
    return True


@app.get("/readyz")
def readyness():
    return True


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
