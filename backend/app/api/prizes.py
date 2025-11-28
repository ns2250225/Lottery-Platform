from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import Prize, PrizeCreate
from app.services.services import PrizeService

router = APIRouter()

@router.get("/raffle/{raffle_id}", response_model=List[Prize])
def get_prizes_by_raffle(raffle_id: int, db: Session = Depends(get_db)):
    """获取抽奖活动的奖品列表"""
    return PrizeService.get_prizes_by_raffle(db, raffle_id)

@router.get("/{prize_id}", response_model=Prize)
def get_prize(prize_id: int, db: Session = Depends(get_db)):
    """获取奖品详情"""
    prize = PrizeService.get_prize_by_id(db, prize_id)
    if not prize:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="奖品不存在"
        )
    return prize

@router.post("/", response_model=Prize, status_code=status.HTTP_201_CREATED)
def create_prize(prize: PrizeCreate, db: Session = Depends(get_db)):
    """创建奖品"""
    return PrizeService.create_prize(db, prize)

@router.put("/{prize_id}", response_model=Prize)
def update_prize(prize_id: int, prize_data: dict, db: Session = Depends(get_db)):
    """更新奖品"""
    prize = PrizeService.update_prize(db, prize_id, prize_data)
    if not prize:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="奖品不存在"
        )
    return prize

@router.delete("/{prize_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prize(prize_id: int, db: Session = Depends(get_db)):
    """删除奖品"""
    success = PrizeService.delete_prize(db, prize_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="奖品不存在"
        )