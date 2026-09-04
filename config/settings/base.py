from pathlib import Path

from decouple import Csv, config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost", cast=Csv())

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "tinymce",
    "django_htmx",
    "src.core",
    "src.pages",
    "src.services",
    "src.faq",
    "src.leads",
    "src.calculator",
    "src.careers",
    "src.social_proof",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "src.core.middleware.CollapseLanguagePrefixMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "src.core.context_processors.site_chrome",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uk"
LANGUAGES = [
    ("uk", "Українська"),
    ("en", "English"),
]
PREFIX_LANGUAGES = ("en",)
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@privat-trans.local")

LEAD_NOTIFY_EMAIL = config("LEAD_NOTIFY_EMAIL", default="")
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default="")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID", default="")
CRM_WEBHOOK_URL = config("CRM_WEBHOOK_URL", default="")

CONTENT_SECURITY_POLICY = {
    # Alpine.js (Unfold) needs unsafe-eval; admin is staff-only.
    "EXCLUDE_URL_PREFIXES": ("/admin/",),
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'", "https://www.googletagmanager.com"),
        "style-src": ("'self'", "https://fonts.googleapis.com"),
        "font-src": ("'self'", "https://fonts.gstatic.com"),
        "img-src": ("'self'", "data:", "https:"),
        "media-src": ("'self'",),
        "connect-src": ("'self'",),
        "frame-src": ("'self'", "https://www.google.com", "https://www.openstreetmap.org"),
        "frame-ancestors": ("'self'",),
        "form-action": ("'self'",),
        "base-uri": ("'self'",),
    },
}

TINYMCE_DEFAULT_CONFIG = {
    "height": 320,
    "menubar": False,
    "plugins": "link lists code",
    "toolbar": "undo redo | bold italic underline | bullist numlist | link | removeformat | code",
    "content_css": False,
    "skin": "oxide",
    "branding": False,
    "promotion": False,
    "browser_spellcheck": True,
}

UNFOLD = {
    "SITE_TITLE": "ПРИВАТ-ТРАНС",
    "SITE_HEADER": "ПРИВАТ-ТРАНС — Адмінпанель",
    "SITE_SYMBOL": "local_shipping",
    "SHOW_HISTORY": True,
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Налаштування",
                "items": [
                    {
                        "title": "Сайт",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                    },
                    {
                        "title": "SEO сторінок",
                        "icon": "travel_explore",
                        "link": reverse_lazy("admin:core_pageseo_changelist"),
                    },
                ],
            },
            {
                "title": "Контент сторінок",
                "separator": True,
                "items": [
                    {
                        "title": "Головна — Hero",
                        "icon": "image",
                        "link": reverse_lazy("admin:core_homeherosettings_changelist"),
                    },
                    {
                        "title": "Головна — Сценарії",
                        "icon": "view_agenda",
                        "link": reverse_lazy("admin:core_homescenariossettings_changelist"),
                    },
                    {
                        "title": "Про нас",
                        "icon": "info",
                        "link": reverse_lazy("admin:core_aboutpagesettings_changelist"),
                    },
                    {
                        "title": "Контакти",
                        "icon": "call",
                        "link": reverse_lazy("admin:core_contactspagesettings_changelist"),
                    },
                    {
                        "title": "Політика",
                        "icon": "policy",
                        "link": reverse_lazy("admin:core_privacypagesettings_changelist"),
                    },
                    {
                        "title": "Послуги (сторінка)",
                        "icon": "view_list",
                        "link": reverse_lazy("admin:core_servicespagesettings_changelist"),
                    },
                    {
                        "title": "FAQ (сторінка)",
                        "icon": "quiz",
                        "link": reverse_lazy("admin:core_faqpagesettings_changelist"),
                    },
                    {
                        "title": "Калькулятор",
                        "icon": "calculate",
                        "link": reverse_lazy("admin:core_calculatorpagesettings_changelist"),
                    },
                ],
            },
            {
                "title": "Каталог послуг",
                "separator": True,
                "items": [
                    {
                        "title": "Послуги",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:services_service_changelist"),
                    },
                    {
                        "title": "FAQ",
                        "icon": "help",
                        "link": reverse_lazy("admin:faq_faqitem_changelist"),
                    },
                    {
                        "title": "Відгуки",
                        "icon": "rate_review",
                        "link": reverse_lazy("admin:social_proof_review_changelist"),
                    },
                    {
                        "title": "Партнери",
                        "icon": "handshake",
                        "link": reverse_lazy("admin:social_proof_partner_changelist"),
                    },
                    {
                        "title": "Вакансії",
                        "icon": "work",
                        "link": reverse_lazy("admin:careers_vacancy_changelist"),
                    },
                ],
            },
            {
                "title": "Заявки",
                "separator": True,
                "items": [
                    {
                        "title": "Ліди",
                        "icon": "mail",
                        "link": reverse_lazy("admin:leads_lead_changelist"),
                    },
                ],
            },
            {
                "title": "Користувачі",
                "separator": True,
                "items": [
                    {
                        "title": "Користувачі",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Групи",
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "src": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}
