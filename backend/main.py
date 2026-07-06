# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import auth, threads, interactions

app = FastAPI(title="Political Threads API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

# Mount API Routers
app.include_router(auth.router)
app.include_router(threads.router)
app.include_router(interactions.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}