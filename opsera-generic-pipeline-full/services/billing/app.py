from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from services.common.auth import require_api_key

app = FastAPI(title="Billing Service", version="0.1.0")

class Invoice(BaseModel):
    invoiceId: str
    customerId: str
    amount: float
    currency: str = "USD"
    status: str

MOCK_INVOICES = [
    Invoice(invoiceId="INV-1001", customerId="CUST-1", amount=199.0, status="paid"),
    Invoice(invoiceId="INV-1002", customerId="CUST-2", amount=49.0, status="due"),
    Invoice(invoiceId="INV-1003", customerId="CUST-1", amount=9.99, status="paid"),
]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "billing"}

@app.get("/billing/invoices", response_model=List[Invoice], dependencies=[Depends(require_api_key)])
def list_invoices(customerId: Optional[str] = Query(default=None)):
    if customerId:
        return [i for i in MOCK_INVOICES if i.customerId == customerId]
    return MOCK_INVOICES
