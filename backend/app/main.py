from fastapi import FastAPI
from app.routes import boards, lists, cards  # ✅ make sure it's `app`, not `appr`

app = FastAPI()

# include routers
app.include_router(boards.router)
app.include_router(lists.router)
app.include_router(cards.router)

@app.get("/")
async def root():
    return {"message": "Trello Clone API is running!"}

# Programmatic run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)