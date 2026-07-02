from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from .models import CreatePayoutRequest, PayoutResponse, ErrorResponse
from .services import process_payout

app = FastAPI(
    title="Courierist Fintech Payout Service",
    version="1.0.0",
    description="Микросервис для автоматизации выплат курьерам"
)

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    """Обработчик ошибок бизнес-логики."""
    error_content = ErrorResponse(detail=str(exc))
    return JSONResponse(status_code=400, content=error_content.dict())

@app.post("/api/v1/payouts/create", response_model=PayoutResponse, responses={400: {"model": ErrorResponse}})
async def create_payout(payout_request: CreatePayoutRequest):
    """
    Создание новой заявки на выплату.
    Принимает ID курьера, сумму и токен карты.
    """
    try:
        result = await process_payout(payout_request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/payouts/{transaction_id}", response_model=PayoutResponse)
async def get_payout_status(transaction_id: str):
    """Проверка статуса конкретной транзакции по её ID."""
    payout = next((item for item in PAYOUTS_DB.values() if item["transaction_id"] == transaction_id), None)
    if not payout:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return PayoutResponse(**payout)