from fastapi import FastAPI

app = FastAPI(title="Trello Clone API")

@app.get("/")
def root():
    return {"message": "Backend running!"}