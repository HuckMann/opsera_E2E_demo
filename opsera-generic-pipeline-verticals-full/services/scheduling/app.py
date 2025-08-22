import os
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from services.common.auth import require_auth

app = FastAPI(title="Scheduling Service", version="0.2.0")

class Slot(BaseModel):
    resourceId: str
    date: str
    start: str
    end: str
    available: bool = True
    label: str | None = None

class AppointmentRequest(BaseModel):
    resourceId: str
    date: str
    start: str
    end: str
    customerId: str

class AppointmentResponse(BaseModel):
    appointmentId: str
    status: str

VERTICAL = os.getenv("VERTICAL", "").lower()

DEFAULT_SLOTS = [
    Slot(resourceId="RES-1", date="2025-08-22", start="09:00", end="09:30", label="Resource 1"),
    Slot(resourceId="RES-1", date="2025-08-22", start="09:30", end="10:00", label="Resource 1"),
    Slot(resourceId="RES-2", date="2025-08-22", start="10:00", end="10:30", label="Resource 2"),
]

HEALTHCARE_SLOTS = [
    Slot(resourceId="DR-KIM", date="2025-08-22", start="09:00", end="09:30", label="Dr. Kim – Pediatrics"),
    Slot(resourceId="DR-KIM", date="2025-08-22", start="09:30", end="10:00", label="Dr. Kim – Pediatrics"),
    Slot(resourceId="DR-LEE", date="2025-08-22", start="10:00", end="10:30", label="Dr. Lee – Cardiology"),
]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "scheduling"}

@app.get("/scheduling/slots", response_model=List[Slot], dependencies=[Depends(lambda: require_auth(["scheduling:read"]))])
def get_slots(resourceId: Optional[str] = Query(default=None), date: Optional[str] = Query(default=None)):
    slots = HEALTHCARE_SLOTS if VERTICAL == "healthcare" else DEFAULT_SLOTS
    if resourceId:
        slots = [s for s in slots if s.resourceId == resourceId]
    if date:
        slots = [s for s in slots if s.date == date]
    return slots

@app.post("/scheduling/appointments", response_model=AppointmentResponse, dependencies=[Depends(lambda: require_auth(["scheduling:write"]))])
def create_appt(req: AppointmentRequest):
    return AppointmentResponse(appointmentId="APT-{}".format(abs(hash(req.customerId)) % 100000), status="booked")
