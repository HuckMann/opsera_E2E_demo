import os
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from services.common.auth import require_auth

app = FastAPI(title="Inventory Service", version="0.2.0")

class Item(BaseModel):
    sku: str
    name: str
    quantity: int

VERTICAL = os.getenv("VERTICAL", "").lower()

DEFAULT_DB = [
    Item(sku="SKU-1001", name="Widget A", quantity=120),
    Item(sku="SKU-1002", name="Widget B", quantity=45),
    Item(sku="SKU-2001", name="Gadget C", quantity=0),
]

RETAIL_DB = [
    Item(sku="TV-55UQ", name="4K UHD TV 55"", quantity=7),
    Item(sku="PHN-ULTRA", name="Smartphone Ultra 256GB", quantity=12),
    Item(sku="SNEAK-RED-10", name="Sneakers Red Size 10", quantity=3),
    Item(sku="JKT-NYLON-L", name="Nylon Jacket Large", quantity=28),
]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "inventory"}

@app.get("/inventory/items", response_model=List[Item], dependencies=[Depends(lambda: require_auth(["inventory:read"]))])
def list_items(
    sku: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=1000),
    lowStockOnly: bool = Query(default=False),
    threshold: int = Query(default=10, ge=1, le=1000),
):
    items = RETAIL_DB if VERTICAL == "retail" else DEFAULT_DB
    if sku:
        items = [i for i in items if i.sku == sku]
    if lowStockOnly:
        items = [i for i in items if i.quantity < threshold]
    return items[:limit]
