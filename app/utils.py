from passlib.context import CryptContext
from random import randint
import os
import httpx
from dotenv import load_dotenv
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SENDINBLUE_API_KEY = os.getenv("SENDINBLUE_API_KEY")

def hashed(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_otp():
    return f"{randint(100000, 999999)}"

async def send_otp_email(to_email: str, otp: str):
    url = "https://api.brevo.com/v3/smtp/email"
    subject = "🔐 Code OTP pour réinitialisation de mot de passe"
    html_content = f"""
    <div>
      <h2>Bonjour,</h2>
      <p>Voici votre code OTP pour réinitialiser votre mot de passe :</p>
      <h3>{otp}</h3>
      <p>Ce code est valable 5 minutes.</p>
      <p>Si vous n'avez pas demandé ce code, veuillez ignorer cet email.</p>
    </div>
    """
    data = {
        "sender": {
            "name": "Groupe Genetics Support",
            "email": "diallo30amadoukorka@gmail.com"
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content,
    }
    headers = {
        "api-key": SENDINBLUE_API_KEY,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()
    

async def send_incident_alert_email(incident, user):
    url = "https://api.brevo.com/v3/smtp/email"
    subject = "🚨 Nouvel incident signalé sur la plateforme Groupe Genetics"

    html_content = f"""
    <div style="font-family: Arial, sans-serif;">
      <h2>🚨 Un nouvel incident a été signalé</h2>
      <p><strong><u>Détails de l'incident</u></strong></p>
      <ul>
        <li><strong>Titre :</strong> {incident.title}</li>
        <li><strong>Description :</strong> {incident.description}</li>
        <li><strong>Priorité :</strong> {incident.priority.value}</li>
        <li><strong>Catégorie :</strong> {incident.category.value}</li>
        <li><strong>Date :</strong> {incident.createdAt.strftime('%Y-%m-%d %H:%M:%S')}</li>
      </ul>
      <p><strong><u>Informations de l'utilisateur</u></strong></p>
      <ul>
        <li><strong>Nom :</strong> {user.name}</li>
        <li><strong>Email :</strong> {user.email}</li>
        <li><strong>Entreprise :</strong> {user.company}</li>
        <li><strong>Téléphone :</strong> {user.phone}</li>
      </ul>
    </div>
    """

    data = {
        "sender": {
            "name": "Groupe Genetics",
            "email": "diallo30amadoukorka@gmail.com"  # adresse d’envoi
        },
        "to": [
            {"email": "diallo30amadoukorka@gmail.com"},
            {"email": "mohamed.thialaw@groupegenetics.com"}
        ],  
        "subject": subject,
        "htmlContent": html_content,
    }

    headers = {
        "api-key": SENDINBLUE_API_KEY,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()


async def send_incident_resolved_email(user_email: str, user_name: str, incident_title: str):
    url = "https://api.brevo.com/v3/smtp/email"
    subject = "✅ Votre incident a été résolu"
    html_content = f"""
    <div>
      <h2>Bonjour {user_name},</h2>
      <p>Votre incident intitulé <strong>{incident_title}</strong> a été marqué comme <strong>terminé</strong> par notre équipe.</p>
      <p>Merci de bien vouloir vérifier et tester si le problème est résolu.</p>
      <p>Si vous rencontrez toujours un problème, n’hésitez pas à nous recontacter.</p>
      <br/>
      <p>Cordialement,</p>
      <p>L'équipe Support</p>
    </div>
    """
    data = {
        "sender": {
            "name": "Groupe Genetics Support",
            "email": "diallo30amadoukorka@gmail.com"
        },
        "to": [{"email": user_email}],
        "subject": subject,
        "htmlContent": html_content,
    }
    headers = {
        "api-key": SENDINBLUE_API_KEY,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()
    
    

async def send_contact_email(name: str, email: str, subject: str, message: str):
    url = "https://api.brevo.com/v3/smtp/email"
    html_content = f"""
    <div>
      <h2>📩 Nouveau message de contact</h2>
      <p><strong>Nom :</strong> {name}</p>
      <p><strong>Email :</strong> {email}</p>
      <p><strong>Sujet :</strong> {subject}</p>
      <p><strong>Message :</strong></p>
      <p>{message}</p>
    </div>
    """
    data = {
        "sender": {
            "name": name,
            "email": email  
        },
        "to": [
            {"email": "diallo30amadoukorka@gmail.com"},  # CEO
        ],
        "subject": f"📩 Message de contact : {subject}",
        "htmlContent": html_content,
    }
    headers = {
        "api-key": SENDINBLUE_API_KEY,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()

