from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from services.common.auth import require_api_key

app = FastAPI(title="Scheduling Service", version="0.1.0")

class Slot(BaseModel):
    resourceId: str
    date: str
    start: str
    end: str
    available: bool = True

class AppointmentRequest(BaseModel):
    resourceId: str
    date: str
    start: str
    end: str
    customerId: str

class AppointmentResponse(BaseModel):
    appointmentId: str
    status: str

MOCK_SLOTS = [
    Slot(resourceId="RES-1", date="2025-08-22", start="09:00", end="09:30"),
    Slot(resourceId="RES-1", date="2025-08-22", start="09:30", end="10:00"),
    Slot(resourceId="RES-2", date="2025-08-22", start="10:00", end="10:30"),
]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "scheduling"}

@app.get("/scheduling/slots", response_model=List[Slot], dependencies=[Depends(require_api_key)])
def get_slots(resourceId: Optional[str] = Query(default=None), date: Optional[str] = Query(default=None)):
    slots = MOCK_SLOTS
    if resourceId:
        slots = [s for s in slots if s.resourceId == resourceId]
    if date:
        slots = [s for s in slots if s.date == date]
    return slots

@app.post("/scheduling/appointments", response_model=AppointmentResponse, dependencies=[Depends(require_api_key)])
def create_appt(req: AppointmentRequest):
    return AppointmentResponse(appointmentId="APT-{}".format(abs(hash(req.customerId)) % 100000), status="booked")
