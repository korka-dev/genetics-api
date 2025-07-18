from fastapi import APIRouter, HTTPException, status
from app.schemas.contact import ContactMessage
from app.utils import send_contact_email

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/send-email", status_code=status.HTTP_200_OK)
async def contact_company(message: ContactMessage):
    try:
        await send_contact_email(
            name=message.name,
            email=message.email,
            subject=message.subject,
            message=message.message
        )
        return {"message": "Votre message a été envoyé avec succès. Nous vous contacterons bientôt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'envoi de l'email : {str(e)}")

