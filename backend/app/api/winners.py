from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import Winner, RaffleDrawRequest, RaffleDrawResult
from app.services.services import WinnerService, DrawService

router = APIRouter()

@router.get("/raffle/{raffle_id}", response_model=List[Winner])
def get_winners_by_raffle(raffle_id: int, db: Session = Depends(get_db)):
    """获取抽奖活动的中奖者列表"""
    return WinnerService.get_winners_by_raffle(db, raffle_id)