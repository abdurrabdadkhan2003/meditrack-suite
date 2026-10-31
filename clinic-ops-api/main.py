from datetime import timedelta
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import models
import schemas

from database import engine, get_db
from middleware import RequestLoggingMiddleware
from exceptions import ResourceNotFoundError, resource_not_found_handler


# ============================================================
# Database
# ============================================================

# Alembic should normally manage your database schema.
# This is kept only to ensure SQLAlchemy models are mapped.
models.Base.metadata.create_all(bind=engine)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Meditrack Clinic Ops API",
    description=(
        "RESTful API for Checklife clinic operations, "
        "scheduling, and patient management."
    ),
    version="1.0.0",
    contact={
        "name": "Maazz (Abdur Rab)",
        "email": "admin@checklife-synthetic.internal",
    },
)


# ============================================================
# Middleware
# ============================================================

app.add_middleware(RequestLoggingMiddleware)


# ============================================================
# Exception Handlers
# ============================================================

app.add_exception_handler(
    ResourceNotFoundError,
    resource_not_found_handler,
)


# ============================================================
# Authentication
# ============================================================

@app.post(
    "/login",
    response_model=auth.Token,
    tags=["Authentication"],
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_dict = auth.FAKE_USERS_DB.get(form_data.username)

    if not user_dict or not auth.verify_password(
        form_data.password,
        user_dict["hashed_password"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(
        minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = auth.create_access_token(
        data={
            "sub": user_dict["username"],
            "role": user_dict["role"],
        },
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ============================================================
# Patients
# ============================================================

@app.get(
    "/patients",
    response_model=List[schemas.PatientResponse],
    tags=["Patients"],
)
def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    patients = (
        db.query(models.Patient)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return patients


@app.get(
    "/patients/{patient_id}",
    response_model=schemas.PatientResponse,
    tags=["Patients"],
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
):
    patient = (
        db.query(models.Patient)
        .filter(models.Patient.patient_id == patient_id)
        .first()
    )

    if not patient:
        raise ResourceNotFoundError(
            resource_name="Patient",
            resource_id=patient_id,
        )

    return patient


@app.post(
    "/patients",
    response_model=schemas.PatientResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Patients"],
)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
):
    db_patient = models.Patient(
        **patient.model_dump()
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient


@app.put(
    "/patients/{patient_id}",
    response_model=schemas.PatientResponse,
    tags=["Patients"],
)
def update_patient(
    patient_id: int,
    patient_update: schemas.PatientUpdate,
    db: Session = Depends(get_db),
):
    db_patient = (
        db.query(models.Patient)
        .filter(models.Patient.patient_id == patient_id)
        .first()
    )

    if not db_patient:
        raise ResourceNotFoundError(
            resource_name="Patient",
            resource_id=patient_id,
        )

    update_data = patient_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)

    return db_patient


@app.delete(
    "/patients/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Patients"],
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: auth.TokenData = Depends(auth.require_admin),
):
    db_patient = (
        db.query(models.Patient)
        .filter(models.Patient.patient_id == patient_id)
        .first()
    )

    if not db_patient:
        raise ResourceNotFoundError(
            resource_name="Patient",
            resource_id=patient_id,
        )

    db.delete(db_patient)
    db.commit()

    return None


# ============================================================
# Visits
# ============================================================

@app.get(
    "/visits",
    response_model=List[schemas.VisitResponse],
    tags=["Visits"],
)
def get_visits(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Visit)

    if patient_id is not None:
        query = query.filter(
            models.Visit.patient_id == patient_id
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.post(
    "/visits",
    response_model=schemas.VisitResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Visits"],
)
def create_visit(
    visit: schemas.VisitCreate,
    db: Session = Depends(get_db),
):
    db_visit = models.Visit(
        **visit.model_dump()
    )

    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)

    return db_visit


# ============================================================
# Appointments
# ============================================================

@app.get(
    "/appointments",
    response_model=List[schemas.AppointmentResponse],
    tags=["Appointments"],
)
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    staff_id: Optional[int] = None,
    appointment_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Appointment)

    if staff_id is not None:
        query = query.filter(
            models.Appointment.staff_id == staff_id
        )

    if appointment_status:
        query = query.filter(
            models.Appointment.status == appointment_status
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.post(
    "/appointments",
    response_model=schemas.AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Appointments"],
)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
):
    db_appointment = models.Appointment(
        **appointment.model_dump()
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment
