import firebase_admin
from firebase_admin import credentials
from firebase_admin.exceptions import UnavailableError
from firebase_admin.messaging import (
    Message,
    Notification,
    send,
    UnregisteredError,
    QuotaExceededError,
)
from config import settings
from exceptions.fcm_quota_exceeded_exception import FCMQuotaExceededException
from exceptions.fcm_service_unavailable_exception import FCMServiceUnavailableException
from exceptions.invalid_fcm_token_exception import InvalidFcmTokenException

def init_firebase_sdk():
    firebase_credentials = credentials.Certificate(settings.firebase_application_credentials)
    firebase_admin.initialize_app(firebase_credentials)
    
def send_push_notification(fcm_token: str, title: str, body: str):
    message = Message(
        notification=Notification(
            title=title,
            body=body,
        ),
        token=fcm_token
    )
    try:
        send(message)
    except UnregisteredError:
        raise InvalidFcmTokenException()
    except UnavailableError:
        raise FCMServiceUnavailableException()
    except QuotaExceededError:
        raise FCMQuotaExceededException()