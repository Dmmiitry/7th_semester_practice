from decimal import Decimal, ROUND_HALF_UP
from .db import PAYOUTS_DB, get_balance, generate_transaction_id, update_balance
from .models import PayoutStatus, CreatePayoutRequest, PayoutResponse
from datetime import datetime

COMMISSION_RATE = 0.015  # Комиссия сервиса 1.5%
MIN_COMMISSION_RUB = 30.0 # Минимальная комиссия 30 рублей

async def process_payout(request: CreatePayoutRequest) -> PayoutResponse:
    """
    Основная функция обработки выплаты.
    Вызов внешнего банковского API.
    """
    
    # 1. Проверка баланса компании
    current_balance = get_balance()
    if request.amount_rub > current_balance:
        raise ValueError("Недостаточно средств на балансе компании для проведения выплаты.")

    # 2. Расчет комиссии и чистой суммы
    calculated_commission = request.amount_rub * COMMISSION_RATE
    final_commission = max(calculated_commission, MIN_COMMISSION_RUB)
    net_amount = request.amount_rub - final_commission
    
    # Переводим в копейки для обновления балансового счета
    debit_amount_kopecks = int((request.amount_rub + final_commission) * 100)
    
    # 3. Блокируем средства (атомарная операция)
    update_balance(debit_amount_kopecks)

    # 4. Создаем запись о транзакции
    transaction_id = generate_transaction_id()
    
    payout_data = {
        "transaction_id": transaction_id,
        "courier_id": request.courier_id,
        "amount_rub": request.amount_rub,
        "status": PayoutStatus.PROCESSING,
        "created_at": datetime.utcnow(),
        "commission_rate": COMMISSION_RATE,
        "net_amount_rub": net_amount,
        "card_token": request.card_token
    }
    PAYOUTS_DB[transaction_id] = payout_data

    # 5. ИМИТАЦИЯ вызова банка (асинхронная задержка)
    # await asyncio.sleep(2) 
    # Пропустим sleep, сразу сменим статус
    
    # Предполагаем, что банк успешно принял запрос
    payout_data["status"] = PayoutStatus.COMPLETED
    
    return PayoutResponse(**payout_data)