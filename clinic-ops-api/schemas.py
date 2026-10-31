from pydantic import BaseModel, constr
from datetime import date, datetime
from typing import Optional

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    contact_number: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    contact_number: Optional[str] = None

class PatientResponse(PatientBase):
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
# --- VISITS ---
class VisitBase(BaseModel):
    patient_id: int
    visit_date: datetime
    reason_for_visit: Optional[str] = None
    notes: Optional[str] = None

class VisitCreate(VisitBase):
    pass

class VisitResponse(VisitBase):
    visit_id: int
    class Config:
        from_attributes = True

# --- APPOINTMENTS ---
class AppointmentBase(BaseModel):
    patient_id: int
    staff_id: int
    scheduled_time: datetime
    status: str = "SCHEDULED"

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    appointment_id: int
    created_at: datetime
    class Config:
        from_attributes = True
