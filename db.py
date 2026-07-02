import uuid
from typing import Dict
from models import PayoutStatus

# Эмуляция таблицы выплат в БД
PAYOUTS_DB: Dict[str, dict] = {}

# Баланс компании (в копейках для точности расчетов)
COMPANY_BALANCE_KOPECKS = 500_0000  # 500 000.00 руб.

def generate_transaction_id() -> str:
    return str(uuid.uuid4())

def get_balance() -> float:
    """Возвращает текущий баланс компании в рублях."""
    return COMPANY_BALANCE_KOPECKS / 100

def update_balance(amount_kopecks: int):
    """Изменяет баланс компании."""
    global COMPANY_BALANCE_KOPECKS
    COMPANY_BALANCE_KOPECKS -= amount_kopecks