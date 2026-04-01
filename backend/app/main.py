from fastapi import FastAPI
from app.routes import boards, lists, cards  # ✅ make sure it's `app`, not `appr`

app = FastAPI()

# include routers
app.include_router(boards.router, prefix="/boards", tags=["boards"])
app.include_router(lists.router, prefix="/lists", tags=["lists"])
app.include_router(cards.router, prefix="/cards", tags=["cards"])

@app.get("/")
async def root():
    return {"message": "Trello Clone API is running!"}

# Programmatic run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)