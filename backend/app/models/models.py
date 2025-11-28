from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class RaffleStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"

class Raffle(Base):
    __tablename__ = "raffles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(RaffleStatus), default=RaffleStatus.NOT_STARTED)
    creator_name = Column(String(50), nullable=False, comment="创建人姓名")
    creator_contact = Column(String(100), nullable=False, comment="创建人联系方式")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    prizes = relationship("Prize", back_populates="raffle")
    participants = relationship("Participant", back_populates="raffle")
    winners = relationship("Winner", back_populates="raffle")

class Prize(Base):
    __tablename__ = "prizes"
    
    id = Column(Integer, primary_key=True, index=True)
    raffle_id = Column(Integer, ForeignKey("raffles.id"), nullable=False)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    level = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    raffle = relationship("Raffle", back_populates="prizes")
    winners = relationship("Winner", back_populates="prize")

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    raffle_id = Column(Integer, ForeignKey("raffles.id"), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    raffle = relationship("Raffle", back_populates="participants")
    winners = relationship("Winner", back_populates="participant")

class Winner(Base):
    __tablename__ = "winners"
    
    id = Column(Integer, primary_key=True, index=True)
    raffle_id = Column(Integer, ForeignKey("raffles.id"), nullable=False)
    prize_id = Column(Integer, ForeignKey("prizes.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    raffle = relationship("Raffle", back_populates="winners")
    prize = relationship("Prize", back_populates="winners")
    participant = relationship("Participant", back_populates="winners")