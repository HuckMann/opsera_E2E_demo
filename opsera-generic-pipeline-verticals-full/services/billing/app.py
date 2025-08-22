import os
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from services.common.auth import require_auth

app = FastAPI(title="Billing Service", version="0.2.0")

class Invoice(BaseModel):
    invoiceId: str
    customerId: str
    amount: float
    currency: str = "USD"
    status: str
    maskedAccount: str | None = None

VERTICAL = os.getenv("VERTICAL", "").lower()

DEFAULT = [
    Invoice(invoiceId="INV-1001", customerId="CUST-1", amount=199.0, status="paid"),
    Invoice(invoiceId="INV-1002", customerId="CUST-2", amount=49.0, status="due"),
    Invoice(invoiceId="INV-1003", customerId="CUST-1", amount=9.99, status="paid"),
]

FINTECH = [
    Invoice(invoiceId="INV-2001", customerId="CUST-1", amount=20.00, status="paid", maskedAccount="**** **** **** 1234"),
    Invoice(invoiceId="INV-2002", customerId="CUST-2", amount=80.50, status="due", maskedAccount="**** **** **** 5678"),
]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "billing"}

@app.get("/billing/invoices", response_model=List[Invoice], dependencies=[Depends(lambda: require_auth(["billing:read"]))])
def list_invoices(customerId: Optional[str] = Query(default=None)):
    data = FINTECH if VERTICAL == "fintech" else DEFAULT
    if customerId:
        return [i for i in data if i.customerId == customerId]
    return data
