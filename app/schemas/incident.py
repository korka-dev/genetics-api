from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum
from datetime import date

class Priority(str, Enum):
    FAIBLE = "FAIBLE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"

class Category(str, Enum):
    RESEAU = "RESEAU"
    SECURITE = "SECURITE"
    LOGICIEL = "LOGICIEL"
    MATERIEL = "MATERIEL"
    ACCES = "ACCES"
    SURVEILLANCE = "SURVEILLANCE"
    AUTRE = "AUTRE"

class IncidentStatus(str, Enum):
    EN_ATTENTE = "EN_ATTENTE"
    EN_TRAITEMENT = "EN_TRAITEMENT"
    TERMINE = "TERMINE"


class IncidentBase(BaseModel):
    title: str
    description: str
    priority: Priority
    category: Category


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: Priority | None = None
    category: Category | None = None
    status: IncidentStatus | None = None


class IncidentOut(IncidentBase):
    id: UUID
    status: IncidentStatus
    createdAt: datetime
    updatedAt: datetime
    userId: UUID

    class Config:
        from_attributes = True


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus

    
    
class DateRange(BaseModel):
    start_date: date
    end_date: date
