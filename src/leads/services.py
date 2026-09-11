import json
import logging
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from src.leads.models import Lead

logger = logging.getLogger(__name__)

LEAD_RATE_MAX = 5
LEAD_RATE_WINDOW = 600
LEAD_RATE_KEY = "lead-rate:{ip}"


def request_ip(request) -> str:
    real_ip = (request.META.get("HTTP_X_REAL_IP") or "").strip()
    if real_ip:
        return real_ip.split(",")[0].strip()
    return (request.META.get("REMOTE_ADDR") or "").strip()


def is_lead_rate_limited(ip: str) -> bool:
    if not ip:
        return False
    return int(cache.get(LEAD_RATE_KEY.format(ip=ip), 0) or 0) >= LEAD_RATE_MAX


def record_lead_submission(ip: str) -> None:
    if not ip:
        return
    key = LEAD_RATE_KEY.format(ip=ip)
    if cache.add(key, 1, LEAD_RATE_WINDOW):
        return
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, LEAD_RATE_WINDOW)


def notify_lead(lead: Lead) -> None:
    body = (
        f"Нова заявка #{lead.pk}\n"
        f"{lead.name} · {lead.phone} · {lead.email}\n"
        f"{lead.from_city} → {lead.to_city}\n"
        f"{lead.cargo} / {lead.service}\n"
        f"{lead.message}"
    )
    if settings.LEAD_NOTIFY_EMAIL:
        try:
            send_mail(
                subject=f"Заявка ПРИВАТ-ТРАНС #{lead.pk}",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.LEAD_NOTIFY_EMAIL],
                fail_silently=True,
            )
        except Exception:
            logger.exception("Lead email notify failed")

    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if token and chat_id:
        payload = json.dumps({"chat_id": chat_id, "text": body}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=8)
        except Exception:
            logger.exception("Lead telegram notify failed")

    webhook = settings.CRM_WEBHOOK_URL
    if webhook:
        payload = json.dumps(
            {
                "status": "Новий лід",
                "name": lead.name,
                "phone": lead.phone,
                "email": lead.email,
                "from": lead.from_city,
                "to": lead.to_city,
                "cargo": lead.cargo,
                "service": lead.service,
                "message": lead.message,
            }
        ).encode()
        req = urllib.request.Request(
            webhook,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=8)
        except Exception:
            logger.exception("Lead CRM webhook failed")
