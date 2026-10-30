import firebase_admin
from firebase_admin import messaging, credentials
from config import settings

def init_firebase_sdk():
    firebase_credentials = credentials.Certificate(settings.firebase_application_credentials)
    firebase_admin.initialize_app(firebase_credentials)
    
def send_push_notification(fcm_token: str, title: str, body: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=fcm_token
    )
    messaging.send(message)