from bs4 import BeautifulSoup
from .common import get_html, clean, abs_url

BASE = "https://berlinstartupjobs.com"

def scrape_berlinstartupjobs(term: str):
    url = f"{BASE}/skill-areas/{term}/"
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    jobs = []

    # 직무 제목 링크는 보통 h4 > a (fallback h3) :contentReference[oaicite:1]{index=1}
    title_links = soup.select("h4 a[href]") or soup.select("h3 a[href]")

    for a in title_links:
        title = clean(a.get_text(" ", strip=True))
        link = abs_url(BASE, a.get("href"))

        if not title or not link:
            continue

        container = a.find_parent("li") or a.find_parent("div") or a.find_parent("section") or a.parent

        company = ""
        company_a = container.select_one('a[href*="/companies/"]') if container else None  # :contentReference[oaicite:2]{index=2}
        if company_a:
            company = clean(company_a.get_text(" ", strip=True))

        jobs.append({
            "source": "berlinstartupjobs.com",
            "title": title,
            "company": company,
            "location": "Berlin/Europe (varies)",
            "reward": "",
            "url": link,
        })

    # url 기준 중복 제거
    uniq = {}
    for j in jobs:
        uniq[j["url"]] = j
    return url, list(uniq.values())