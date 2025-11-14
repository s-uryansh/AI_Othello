from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes_game, routes_training

app = FastAPI(title="AI Othello API")

origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_game.router, prefix="/api/v1/game", tags=["Game"])
app.include_router(routes_training.router, prefix="/api/v1/training", tags=["Training"])

@app.get("/", tags=["Health"])
def root():
    return {"message": "Backend running", "status": "ok"}
