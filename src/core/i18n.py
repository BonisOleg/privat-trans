from urllib.parse import urlencode, urlparse, urlunparse

from django.conf import settings


def prefix_codes() -> tuple[str, ...]:
    default = settings.LANGUAGE_CODE
    return tuple(code for code, _name in settings.LANGUAGES if code != default)


def split_query(path: str) -> tuple[str, str]:
    parsed = urlparse(path)
    clean = parsed.path or "/"
    query = parsed.query
    return clean, query


def join_query(path: str, query: str) -> str:
    if not query:
        return path
    return urlunparse(("", "", path, "", query, ""))


def collapse_double_prefix(path: str) -> str:
    prefixes = prefix_codes()
    clean, query = split_query(path)
    parts = [p for p in clean.split("/") if p]
    while len(parts) >= 2 and parts[0] in prefixes and parts[1] in prefixes:
        parts.pop(0)
    rebuilt = "/" + "/".join(parts)
    if clean.endswith("/") and rebuilt != "/":
        rebuilt += "/"
    return join_query(rebuilt or "/", query)


def strip_language_prefix(path: str) -> str:
    prefixes = prefix_codes()
    clean, query = split_query(path)
    changed = True
    while changed:
        changed = False
        parts = [p for p in clean.split("/") if p]
        if parts and parts[0] in prefixes:
            parts.pop(0)
            clean = "/" + "/".join(parts)
            if not clean.endswith("/") and path.rstrip("?").endswith("/"):
                clean += "/"
            if clean == "":
                clean = "/"
            changed = True
    if not clean.startswith("/"):
        clean = "/" + clean
    return join_query(clean, query)


def localize_path(path: str, lang: str) -> str:
    clean, query = split_query(strip_language_prefix(path))
    if lang == settings.LANGUAGE_CODE:
        localized = clean or "/"
    else:
        if clean == "/":
            localized = f"/{lang}/"
        else:
            localized = f"/{lang}{clean}"
    return join_query(localized, query)


def lang_switch_map(path: str) -> dict[str, str]:
    return {code: localize_path(path, code) for code, _name in settings.LANGUAGES}


def build_query(params: dict[str, str]) -> str:
    return urlencode({k: v for k, v in params.items() if v})
