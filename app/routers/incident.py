from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.postgres_connect import get_db
from app.model import Incident, User
from app.schemas.incident import IncidentCreate, IncidentOut, IncidentStatus, IncidentStatusUpdate, IncidentUpdate
from app.oauth2 import get_current_ceo_user, get_current_user
import asyncio
from app.utils import send_incident_alert_email, send_incident_resolved_email 

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.post("/create-incident", response_model=IncidentOut)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_incident = Incident(**incident.model_dump(), userId=current_user.id)
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    asyncio.run(send_incident_alert_email(new_incident, current_user))

    return new_incident


@router.get("/list-incidents", response_model=list[IncidentOut])
def list_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Incident).filter(Incident.userId == current_user.id).all()

@router.get("/get-incident/{incident_id}", response_model=IncidentOut)
def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter_by(id=incident_id, userId=current_user.id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Incident non trouvé")
    return incident

@router.put("/update-incident/{incident_id}", response_model=IncidentOut)
def update_incident(
    incident_id: UUID,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter_by(id=incident_id, userId=current_user.id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Incident non trouvé")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)

    db.commit()
    db.refresh(incident)
    return incident


@router.delete("/delete-incident/{incident_id}")
def delete_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter_by(id=incident_id, userId=current_user.id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Incident non trouvé")

    db.delete(incident)
    db.commit()
    return {"message": "Incident supprimé avec succès"}


@router.patch("/update-status/{incident_id}", response_model=IncidentOut)
def update_incident_status(
    incident_id: UUID,
    payload: IncidentStatusUpdate,
    db: Session = Depends(get_db),
    __current_ceo: User = Depends(get_current_ceo_user)  # Seul le CEO peut appeler
):
    
    incident = db.query(Incident).filter_by(id=incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident non trouvé")

    incident.status = payload.status
    db.commit()
    db.refresh(incident)

    # Si status est TERMINE, envoi email à l'utilisateur
    if payload.status == IncidentStatus.TERMINE:
        user = incident.user  
        if user:
            # lancer tâche asynchrone pour ne pas bloquer la réponse HTTP
            asyncio.run(send_incident_resolved_email(user.email, user.name, incident.title))

    return incident
