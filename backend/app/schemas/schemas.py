from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.models.models import RaffleStatus

# 抽奖活动相关Schema
class RaffleBase(BaseModel):
    title: str = Field(..., max_length=100, description="活动标题")
    description: Optional[str] = Field(None, description="活动描述")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    creator_name: str = Field(..., max_length=50, description="创建人姓名")
    creator_contact: str = Field(..., max_length=100, description="创建人联系方式")

class RaffleCreate(RaffleBase):
    pass

class RaffleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100, description="活动标题")
    description: Optional[str] = Field(None, description="活动描述")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    status: Optional[RaffleStatus] = Field(None, description="活动状态")

class Raffle(RaffleBase):
    id: int
    status: RaffleStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 奖品相关Schema
class PrizeBase(BaseModel):
    name: str = Field(..., max_length=100, description="奖品名称")
    quantity: int = Field(..., gt=0, description="奖品数量")
    level: int = Field(..., gt=0, description="奖品等级")

class PrizeCreate(PrizeBase):
    raffle_id: int = Field(..., description="抽奖活动ID")

class Prize(PrizeBase):
    id: int
    raffle_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 参与者相关Schema
class ParticipantBase(BaseModel):
    name: str = Field(..., max_length=50, description="参与者姓名")
    email: str = Field(..., max_length=100, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="电话号码")

class ParticipantCreate(ParticipantBase):
    raffle_id: int = Field(..., description="抽奖活动ID")

class Participant(ParticipantBase):
    id: int
    raffle_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 中奖者相关Schema
class WinnerBase(BaseModel):
    raffle_id: int
    prize_id: int
    participant_id: int

class WinnerCreate(WinnerBase):
    pass

class Winner(WinnerBase):
    id: int
    created_at: datetime
    
    # 包含关联信息
    prize: Prize
    participant: Participant
    
    class Config:
        from_attributes = True

# 抽奖活动详情Schema（包含奖品和参与者）
class RaffleDetail(Raffle):
    prizes: List[Prize] = []
    participants: List[Participant] = []
    winners: List[Winner] = []
    
    class Config:
        from_attributes = True

# 抽奖请求Schema
class RaffleDrawRequest(BaseModel):
    raffle_id: int = Field(..., description="抽奖活动ID")
    creator_name: str = Field(..., max_length=50, description="创建人姓名")
    creator_contact: str = Field(..., max_length=100, description="创建人联系方式")

# 抽奖结果Schema
class RaffleDrawResult(BaseModel):
    raffle_id: int
    winners: List[Winner]
    message: str

# 分页响应Schema
class RaffleListResponse(BaseModel):
    items: List[Raffle]
    total: int

# 包含统计信息的抽奖活动Schema
class RaffleWithStats(Raffle):
    participant_count: int = 0
    prize_count: int = 0
    winner_count: int = 0
    
    class Config:
        from_attributes = True

# 包含统计信息的分页响应Schema
class RaffleListResponseWithStats(BaseModel):
    items: List[RaffleWithStats]
    total: int

# 创建人验证Schema
class CreatorVerification(BaseModel):
    creator_name: str = Field(..., max_length=50, description="创建人姓名")
    creator_contact: str = Field(..., max_length=100, description="创建人联系方式")