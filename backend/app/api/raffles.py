from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import RaffleCreate, RaffleUpdate, RaffleDetail, RaffleListResponse, RaffleListResponseWithStats, RaffleDrawRequest, RaffleDrawResult, Raffle as RaffleResponse, CreatorVerification
from app.services.services import RaffleService, DrawService
from app.models.models import Raffle as RaffleModel, RaffleStatus

router = APIRouter()

@router.get("/", response_model=RaffleListResponseWithStats)
def get_raffles(skip: int = 0, limit: int = 100, status: str = "", db: Session = Depends(get_db)):
    """获取抽奖活动列表（包含统计信息）"""
    raffles = RaffleService.get_raffles_with_stats(db, skip=skip, limit=limit, status=status)
    total = RaffleService.get_raffles_count(db, status=status)
    return {
        "items": raffles,
        "total": total
    }

@router.get("/{raffle_id}", response_model=RaffleDetail)
def get_raffle(raffle_id: int, db: Session = Depends(get_db)):
    """获取抽奖活动详情"""
    raffle = RaffleService.get_raffle_detail(db, raffle_id)
    if not raffle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="抽奖活动不存在"
        )
    return raffle

@router.post("/", response_model=RaffleResponse, status_code=status.HTTP_201_CREATED)
def create_raffle(raffle: RaffleCreate, db: Session = Depends(get_db)):
    """创建抽奖活动"""
    return RaffleService.create_raffle(db, raffle)

@router.put("/{raffle_id}", response_model=RaffleResponse)
def update_raffle(raffle_id: int, raffle: RaffleUpdate, db: Session = Depends(get_db)):
    """更新抽奖活动"""
    db_raffle = RaffleService.update_raffle(db, raffle_id, raffle)
    if not db_raffle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="抽奖活动不存在"
        )
    return db_raffle

@router.delete("/{raffle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_raffle(raffle_id: int, db: Session = Depends(get_db)):
    """删除抽奖活动"""
    success = RaffleService.delete_raffle(db, raffle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="抽奖活动不存在"
        )

@router.post("/{raffle_id}/start", response_model=RaffleResponse)
def start_raffle(raffle_id: int, request: CreatorVerification, db: Session = Depends(get_db)):
    """开始抽奖活动"""
    # 验证是否为活动创建人
    raffle = db.query(RaffleModel).filter(RaffleModel.id == raffle_id).first()
    if not raffle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="抽奖活动不存在"
        )
    
    if raffle.creator_name != request.creator_name or raffle.creator_contact != request.creator_contact:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有活动创建人才能开始活动"
        )
    
    raffle = RaffleService.update_raffle_status(db, raffle_id, RaffleStatus.IN_PROGRESS)
    return raffle

@router.post("/{raffle_id}/finish", response_model=RaffleResponse)
def finish_raffle(raffle_id: int, request: CreatorVerification, db: Session = Depends(get_db)):
    """结束抽奖活动"""
    # 验证是否为活动创建人
    raffle = db.query(RaffleModel).filter(RaffleModel.id == raffle_id).first()
    if not raffle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="抽奖活动不存在"
        )
    
    if raffle.creator_name != request.creator_name or raffle.creator_contact != request.creator_contact:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有活动创建人才能结束活动"
        )
    
    raffle = RaffleService.update_raffle_status(db, raffle_id, RaffleStatus.FINISHED)
    return raffle

@router.post("/draw", response_model=RaffleDrawResult)
def draw_raffle(request: RaffleDrawRequest, db: Session = Depends(get_db)):
    """执行抽奖"""
    # 验证是否为活动创建人
    raffle = db.query(RaffleModel).filter(RaffleModel.id == request.raffle_id).first()
    if not raffle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="抽奖活动不存在"
        )
    
    if raffle.creator_name != request.creator_name or raffle.creator_contact != request.creator_contact:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有活动创建人才能执行抽奖"
        )
    
    result = DrawService.draw_raffle(db, request.raffle_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return RaffleDrawResult(
        raffle_id=request.raffle_id,
        winners=result["winners"],
        message=result["message"]
    )