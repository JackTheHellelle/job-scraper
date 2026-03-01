from bs4 import BeautifulSoup
from .common import get_html, clean
from scrapers.common import slugify

BASE = "https://web3.career"

def _abs_url(href: str) -> str:
    if not href:
        return ""
    return href if href.startswith("http") else BASE + href

def scrape_web3career(term: str):
    slug = slugify(term)
    url = f"{BASE}/{slug}-jobs"
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    results = []

    for row in soup.select("tr.table_row"):
        # 1) 상세 URL: onclick 우선, 없으면 a[href]
        onclick = row.get("onclick", "") or ""
        href = ""

        if "tableTurboRowClick" in onclick:
            parts = onclick.split(",")
            if len(parts) >= 2:
                cand = parts[1].strip().strip(")").strip()
                cand = cand.strip("'").strip('"')
                href = cand

        if not href:
            a = row.select_one("a[href]")
            href = a.get("href", "") if a else ""

        job_url = _abs_url(href)
        if not job_url:
            continue

        # 2) title: h2
        title_el = row.select_one("h2")
        title = clean(title_el.get_text(" ", strip=True)) if title_el else ""
        if not title:
            continue

        # 3) company: h3
        company_el = row.select_one("h3")
        company = clean(company_el.get_text(" ", strip=True)) if company_el else ""

        # 4) location:
        #    - 회사 td도 class="job-location-mobile"라서 "h3 있는 td"는 제외
        #    - 위치 td는 (a들) 또는 (span 텍스트) 케이스가 있음
        location = ""
        for td in row.select("td.job-location-mobile"):
            if td.select_one("h3"):  # 회사 td
                continue

            # a 케이스: Amsterdam, Netherlands
            loc_as = [clean(a.get_text(" ", strip=True)) for a in td.select("a")]
            loc_as = [x for x in loc_as if x]
            if loc_as:
                location = ", ".join(loc_as)
                break

            # span 케이스: Asia
            td_text = clean(td.get_text(" ", strip=True))
            if td_text:
                location = td_text
                break

        # 5) reward/salary: 비어있을 수 있음
        reward = ""
        reward_el = row.select_one("p.text-salary")
        if reward_el:
            reward = clean(reward_el.get_text(" ", strip=True))
            # 완전히 빈 <p><span></span></p> 같은 케이스면 "" 유지

        results.append({
            "source": "web3.career",
            "title": title,
            "company": company,
            "location": location,
            "reward": reward,
            "url": job_url,
        })

    # 중복 제거(url)
    uniq = {}
    for r in results:
        uniq[r["url"]] = r

    return url, list(uniq.values())