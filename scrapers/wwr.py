from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from .common import get_html, clean, abs_url, is_ascii_term

BASE = "https://weworkremotely.com"

def scrape_weworkremotely(term: str):
    if not is_ascii_term(term):
        return f"{BASE}/", []

    url = f"{BASE}/remote-jobs/search?term={quote_plus(term)}"
    html = get_html(url, allow_statuses=(403, 429))
    if not html:
        return url, []

    soup = BeautifulSoup(html, "html.parser")

    jobs = []
    # 결과는 보통 section.jobs > article > ul > li 형태
    for li in soup.select("section.jobs li"):
        a = li.select_one("a[href]")
        if not a:
            continue

        href = a.get("href", "")
        # 검색 결과에는 광고/탭/빈 li도 있을 수 있어 필터링
        if not href.startswith("/remote-jobs/"):
            continue

        job_url = abs_url(BASE, href)

        # title/company/location 대략적인 셀렉터들 (사이트 변동 대비)
        company = clean((li.select_one("span.company") or li.select_one(".company")).get_text(" ", strip=True)) if (li.select_one("span.company") or li.select_one(".company")) else ""
        title = clean((li.select_one("span.title") or li.select_one(".title")).get_text(" ", strip=True)) if (li.select_one("span.title") or li.select_one(".title")) else ""
        location = clean((li.select_one("span.region") or li.select_one(".region")).get_text(" ", strip=True)) if (li.select_one("span.region") or li.select_one(".region")) else ""

        if not title or not job_url:
            continue

        jobs.append({
            "source": "weworkremotely.com",
            "title": title,
            "company": company,
            "location": location,
            "reward": "",
            "url": job_url,
        })

    uniq = {}
    for j in jobs:
        uniq[j["url"]] = j
    return url, list(uniq.values())