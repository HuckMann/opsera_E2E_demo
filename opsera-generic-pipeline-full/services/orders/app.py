from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import List
from services.common.auth import require_api_key

app = FastAPI(title="Orders Service", version="0.1.0")

class OrderItem(BaseModel):
    sku: str
    quantity: int = Field(ge=1)

class OrderRequest(BaseModel):
    customerId: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    orderId: str
    status: str

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "orders"}

@app.post("/orders", response_model=OrderResponse, dependencies=[Depends(require_api_key)])
def create_order(payload: OrderRequest):
    return OrderResponse(orderId="ORD-{}".format(hash(payload.customerId) % 100000), status="accepted")
