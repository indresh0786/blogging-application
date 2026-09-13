import json
from pywebpush import webpush
from django.conf import settings

from .models import PushSubscription


def send_push_notification(title, message, url="/"):
    payload = json.dumps({
        "title": title,
        "body": message,
        "url": url,
    })

    subscriptions = PushSubscription.objects.all()

    for subscription in subscriptions:
        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh,
                "auth": subscription.auth,
            },
        }

        try:
            webpush(
                subscription_info=subscription_info,
                data=payload,
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": settings.VAPID_SUBJECT,
                },
            )
        except Exception as e:
            print("Push notification error:", e)