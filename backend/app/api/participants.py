from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import Participant, ParticipantCreate
from app.services.services import ParticipantService

router = APIRouter()

@router.get("/raffle/{raffle_id}", response_model=List[Participant])
def get_participants_by_raffle(raffle_id: int, db: Session = Depends(get_db)):
    """获取抽奖活动的参与者列表"""
    return ParticipantService.get_participants_by_raffle(db, raffle_id)

@router.get("/{participant_id}", response_model=Participant)
def get_participant(participant_id: int, db: Session = Depends(get_db)):
    """获取参与者详情"""
    participant = ParticipantService.get_participant_by_id(db, participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="参与者不存在"
        )
    return participant

@router.post("/", response_model=Participant, status_code=status.HTTP_201_CREATED)
def create_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    """创建参与者（参与抽奖）"""
    # 检查是否已参与（基于姓名+邮箱的组合）
    if ParticipantService.check_duplicate_participant_by_email(db, participant.raffle_id, participant.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已参与此抽奖活动"
        )
    
    return ParticipantService.create_participant(db, participant)