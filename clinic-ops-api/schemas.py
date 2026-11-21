from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# --- PATIENTS ---
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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


# --- INVOICES ---
class InvoiceBase(BaseModel):
    patient_id: int
    appointment_id: Optional[int] = None
    amount: float
    status: str = "ISSUED"


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceResponse(InvoiceBase):
    invoice_id: int
    issued_date: datetime
    paid_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# --- CLAIMS ---
class ClaimBase(BaseModel):
    invoice_id: int
    claim_code: str
    claim_amount: float
    status: str = "SUBMITTED"


class ClaimCreate(ClaimBase):
    pass


class ClaimResponse(ClaimBase):
    claim_id: int
    submission_date: datetime
    adjudicated_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
