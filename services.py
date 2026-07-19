import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

BEEM_URL = "https://apisms.beem.africa/v1/send"


def send_sms(phone: str, message: str) -> bool:
    """
    Send an SMS via Beem Africa.
    phone: international format, e.g. '255758523353'
    """
    phone = phone.strip().lstrip('+')
    if phone.startswith('0'):
        phone = '255' + phone[1:]

    payload = {
        "source_addr": settings.BEEM_SENDER_ID,
        "encoding": 0,
        "message": message,
        "recipients": [
            {"recipient_id": 1, "dest_addr": phone}
        ],
    }

    try:
        response = requests.post(
            BEEM_URL,
            json=payload,
            auth=HTTPBasicAuth(settings.BEEM_API_KEY, settings.BEEM_SECRET_KEY),
            timeout=10,
        )
        return response.status_code == 200
    except requests.RequestException as e:
        logger.error(f"SMS failed for {phone}: {e}")
        return False
