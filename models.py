from pydantic import BaseModel, Field, constr
from typing import Literal
from datetime import datetime

class CreatePayoutRequest(BaseModel):
    """Схема входящего запроса на создание выплаты курьеру."""
    courier_id: int = Field(..., description="Уникальный идентификатор курьера")
    amount_rub: float = Field(..., gt=0, description="Сумма к выплате в рублях")
    card_token: constr(min_length=10) = Field(..., description="Токен банковской карты")

class PayoutStatus(str):
    """Статусы транзакции."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class PayoutResponse(BaseModel):
    """Схема ответа сервера после создания выплаты."""
    transaction_id: str
    courier_id: int
    amount_rub: float
    status: PayoutStatus
    created_at: datetime
    commission_rate: float
    net_amount_rub: float

class ErrorResponse(BaseModel):
    """Схема сообщения об ошибке."""
    detail: str