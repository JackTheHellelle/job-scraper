import re
from urllib.parse import urljoin
import requests

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def get_html(
    url: str,
    timeout: int = 20,
    allow_404: bool = False,
    allow_statuses: tuple[int, ...] = (),
) -> str:
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

    # 특정 상태코드는 "사이트가 막았거나 없음"으로 보고 그냥 빈 페이지 처리
    if r.status_code == 404 and allow_404:
        return ""

    if r.status_code in allow_statuses:
        return ""

    r.raise_for_status()
    return r.text

def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()

def slugify(term: str) -> str:
    term = clean(term).lower()
    term = re.sub(r"[^a-z0-9]+", "-", term)
    term = re.sub(r"-{2,}", "-", term).strip("-")
    return term

def abs_url(base: str, href: str) -> str:
    return urljoin(base, href or "")

def is_ascii_term(term: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9._\-\s]+", term or "") is not None