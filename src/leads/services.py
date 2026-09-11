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


def _notify_telegram(body: str) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not (token and chat_id):
        return
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


def _notify_email(body: str, lead_pk: int) -> None:
    if not settings.LEAD_NOTIFY_EMAIL:
        return
    try:
        send_mail(
            subject=f"Заявка ПРИВАТ-ТРАНС #{lead_pk}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.LEAD_NOTIFY_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Lead email notify failed")


def _notify_crm(lead: Lead) -> None:
    webhook = settings.CRM_WEBHOOK_URL
    if not webhook:
        return
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


def notify_lead(lead: Lead) -> None:
    body = (
        f"Нова заявка #{lead.pk}\n"
        f"{lead.name} · {lead.phone} · {lead.email}\n"
        f"{lead.from_city} → {lead.to_city}\n"
        f"{lead.cargo} / {lead.service}\n"
        f"{lead.message}"
    )
    # Telegram першим (короткий timeout): не блокуємо worker на завислому SMTP.
    _notify_telegram(body)
    _notify_email(body, lead.pk)
    _notify_crm(lead)
