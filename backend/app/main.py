from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import raffles, participants, prizes, winners
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="抽奖应用API"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(raffles.router, prefix="/api/raffles", tags=["raffles"])
app.include_router(participants.router, prefix="/api/participants", tags=["participants"])
app.include_router(prizes.router, prefix="/api/prizes", tags=["prizes"])
app.include_router(winners.router, prefix="/api/winners", tags=["winners"])

@app.get("/")
def read_root():
    return {"message": "抽奖应用API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}