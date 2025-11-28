from sqlalchemy.orm import Session
from app.models.models import Raffle, Prize, Participant, Winner, RaffleStatus
from app.schemas.schemas import RaffleCreate, RaffleUpdate, PrizeCreate, ParticipantCreate
from datetime import datetime
from typing import List, Optional
import random

# 抽奖活动服务
class RaffleService:
    @staticmethod
    def get_raffles(db: Session, skip: int = 0, limit: int = 100) -> List[Raffle]:
        return db.query(Raffle).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_raffles_with_stats(db: Session, skip: int = 0, limit: int = 100, status: str = "") -> List[dict]:
        """获取包含统计信息的抽奖活动列表"""
        from app.schemas.schemas import RaffleWithStats
        
        query = db.query(Raffle)
        if status:
            query = query.filter(Raffle.status == status)
        
        raffles = query.offset(skip).limit(limit).all()
        
        result = []
        for raffle in raffles:
            # 计算参与人数
            participant_count = db.query(Participant).filter(
                Participant.raffle_id == raffle.id
            ).count()
            
            # 计算奖品数量
            prize_count = db.query(Prize).filter(
                Prize.raffle_id == raffle.id
            ).count()
            
            # 计算中奖人数
            winner_count = db.query(Winner).filter(
                Winner.raffle_id == raffle.id
            ).count()
            
            # 创建包含统计信息的对象
            raffle_stats = {
                "id": raffle.id,
                "title": raffle.title,
                "description": raffle.description,
                "start_time": raffle.start_time,
                "end_time": raffle.end_time,
                "creator_name": raffle.creator_name,
                "creator_contact": raffle.creator_contact,
                "status": raffle.status,
                "created_at": raffle.created_at,
                "updated_at": raffle.updated_at,
                "participant_count": participant_count,
                "prize_count": prize_count,
                "winner_count": winner_count
            }
            result.append(raffle_stats)
        
        return result
    
    @staticmethod
    def get_raffles_filtered(db: Session, skip: int = 0, limit: int = 100, status: str = "") -> List[Raffle]:
        query = db.query(Raffle)
        if status:
            query = query.filter(Raffle.status == status)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_raffles_count(db: Session, status: str = "") -> int:
        query = db.query(Raffle)
        if status:
            query = query.filter(Raffle.status == status)
        return query.count()
    
    @staticmethod
    def get_raffle_by_id(db: Session, raffle_id: int) -> Optional[Raffle]:
        return db.query(Raffle).filter(Raffle.id == raffle_id).first()
    
    @staticmethod
    def create_raffle(db: Session, raffle: RaffleCreate) -> Raffle:
        db_raffle = Raffle(
            title=raffle.title,
            description=raffle.description,
            start_time=raffle.start_time,
            end_time=raffle.end_time,
            creator_name=raffle.creator_name,
            creator_contact=raffle.creator_contact,
            status=RaffleStatus.NOT_STARTED
        )
        db.add(db_raffle)
        db.commit()
        db.refresh(db_raffle)
        return db_raffle
    
    @staticmethod
    def update_raffle(db: Session, raffle_id: int, raffle: RaffleUpdate) -> Optional[Raffle]:
        db_raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
        if db_raffle:
            update_data = raffle.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_raffle, key, value)
            db.commit()
            db.refresh(db_raffle)
        return db_raffle
    
    @staticmethod
    def delete_raffle(db: Session, raffle_id: int) -> bool:
        db_raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
        if db_raffle:
            db.delete(db_raffle)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_raffle_detail(db: Session, raffle_id: int) -> Optional[Raffle]:
        return db.query(Raffle).filter(Raffle.id == raffle_id).first()
    
    @staticmethod
    def update_raffle_status(db: Session, raffle_id: int, status: RaffleStatus) -> Optional[Raffle]:
        db_raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
        if db_raffle:
            db_raffle.status = status
            db.commit()
            db.refresh(db_raffle)
        return db_raffle

# 奖品服务
class PrizeService:
    @staticmethod
    def get_prizes_by_raffle(db: Session, raffle_id: int) -> List[Prize]:
        return db.query(Prize).filter(Prize.raffle_id == raffle_id).all()
    
    @staticmethod
    def get_prize_by_id(db: Session, prize_id: int) -> Optional[Prize]:
        return db.query(Prize).filter(Prize.id == prize_id).first()
    
    @staticmethod
    def create_prize(db: Session, prize: PrizeCreate) -> Prize:
        db_prize = Prize(
            raffle_id=prize.raffle_id,
            name=prize.name,
            quantity=prize.quantity,
            level=prize.level
        )
        db.add(db_prize)
        db.commit()
        db.refresh(db_prize)
        return db_prize
    
    @staticmethod
    def update_prize(db: Session, prize_id: int, prize_data: dict) -> Optional[Prize]:
        db_prize = db.query(Prize).filter(Prize.id == prize_id).first()
        if db_prize:
            for key, value in prize_data.items():
                setattr(db_prize, key, value)
            db.commit()
            db.refresh(db_prize)
        return db_prize
    
    @staticmethod
    def delete_prize(db: Session, prize_id: int) -> bool:
        db_prize = db.query(Prize).filter(Prize.id == prize_id).first()
        if db_prize:
            db.delete(db_prize)
            db.commit()
            return True
        return False

# 参与者服务
class ParticipantService:
    @staticmethod
    def get_participants_by_raffle(db: Session, raffle_id: int) -> List[Participant]:
        return db.query(Participant).filter(Participant.raffle_id == raffle_id).all()
    
    @staticmethod
    def get_participant_by_id(db: Session, participant_id: int) -> Optional[Participant]:
        return db.query(Participant).filter(Participant.id == participant_id).first()
    
    @staticmethod
    def create_participant(db: Session, participant: ParticipantCreate) -> Participant:
        db_participant = Participant(
            raffle_id=participant.raffle_id,
            name=participant.name,
            phone=participant.phone,
            email=participant.email
        )
        db.add(db_participant)
        db.commit()
        db.refresh(db_participant)
        return db_participant
    
    @staticmethod
    def check_duplicate_participant(db: Session, raffle_id: int, phone: str) -> bool:
        return db.query(Participant).filter(
            Participant.raffle_id == raffle_id,
            Participant.phone == phone
        ).first() is not None
    
    @staticmethod
    def check_duplicate_participant_by_email(db: Session, raffle_id: int, email: str) -> bool:
        return db.query(Participant).filter(
            Participant.raffle_id == raffle_id,
            Participant.email == email
        ).first() is not None

# 中奖者服务
class WinnerService:
    @staticmethod
    def get_winners_by_raffle(db: Session, raffle_id: int) -> List[Winner]:
        return db.query(Winner).filter(Winner.raffle_id == raffle_id).all()
    
    @staticmethod
    def create_winner(db: Session, raffle_id: int, prize_id: int, participant_id: int) -> Winner:
        db_winner = Winner(
            raffle_id=raffle_id,
            prize_id=prize_id,
            participant_id=participant_id
        )
        db.add(db_winner)
        db.commit()
        db.refresh(db_winner)
        return db_winner

# 抽奖服务
class DrawService:
    @staticmethod
    def draw_raffle(db: Session, raffle_id: int) -> dict:
        # 获取抽奖活动
        raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
        if not raffle:
            return {"success": False, "message": "抽奖活动不存在"}
        
        if raffle.status != RaffleStatus.IN_PROGRESS:
            return {"success": False, "message": "抽奖活动未进行中"}
        
        # 获取奖品
        prizes = db.query(Prize).filter(Prize.raffle_id == raffle_id).all()
        if not prizes:
            return {"success": False, "message": "没有设置奖品"}
        
        # 获取参与者
        participants = db.query(Participant).filter(Participant.raffle_id == raffle_id).all()
        if not participants:
            return {"success": False, "message": "没有参与者"}
        
        # 获取已中奖的参与者ID
        existing_winners = db.query(Winner).filter(Winner.raffle_id == raffle_id).all()
        winner_participant_ids = [w.participant_id for w in existing_winners]
        
        # 筛选出未中奖的参与者
        available_participants = [p for p in participants if p.id not in winner_participant_ids]
        
        if not available_participants:
            return {"success": False, "message": "所有参与者都已中奖"}
        
        # 按奖品等级排序，从高等级开始抽
        prizes.sort(key=lambda x: x.level)
        
        new_winners = []
        
        for prize in prizes:
            # 检查该奖品是否已抽完
            prize_winners_count = db.query(Winner).filter(
                Winner.raffle_id == raffle_id,
                Winner.prize_id == prize.id
            ).count()
            
            if prize_winners_count >= prize.quantity:
                continue  # 该奖品已抽完
            
            # 计算还需要抽多少个该奖品
            remaining_prizes = prize.quantity - prize_winners_count
            
            # 随机选择中奖者
            for _ in range(min(remaining_prizes, len(available_participants))):
                if not available_participants:
                    break
                
                winner = random.choice(available_participants)
                available_participants.remove(winner)
                
                # 创建中奖记录
                db_winner = Winner(
                    raffle_id=raffle_id,
                    prize_id=prize.id,
                    participant_id=winner.id
                )
                db.add(db_winner)
                new_winners.append(db_winner)
        
        if not new_winners:
            return {"success": False, "message": "没有足够的参与者进行抽奖"}
        
        db.commit()
        
        # 检查是否所有奖品都已抽完
        all_prizes_drawn = True
        for prize in prizes:
            prize_winners_count = db.query(Winner).filter(
                Winner.raffle_id == raffle_id,
                Winner.prize_id == prize.id
            ).count()
            if prize_winners_count < prize.quantity:
                all_prizes_drawn = False
                break
        
        # 如果所有奖品都已抽完，更新抽奖活动状态为已结束
        if all_prizes_drawn:
            raffle.status = RaffleStatus.FINISHED
            db.commit()
        
        return {
            "success": True,
            "message": "抽奖成功",
            "winners": new_winners
        }