from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from services.common.auth import require_api_key

app = FastAPI(title="Inventory Service", version="0.1.0")

class Item(BaseModel):
    sku: str
    name: str
    quantity: int

MOCK_DB = [
    Item(sku="SKU-1001", name="Widget A", quantity=120),
    Item(sku="SKU-1002", name="Widget B", quantity=45),
    Item(sku="SKU-2001", name="Gadget C", quantity=0),
]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "inventory"}

@app.get("/inventory/items", response_model=List[Item], dependencies=[Depends(require_api_key)])
def list_items(sku: Optional[str] = Query(default=None), limit: int = Query(default=50, ge=1, le=1000)):
    items = MOCK_DB
    if sku:
        items = [i for i in items if i.sku == sku]
    return items[:limit]
