from .berlin import scrape_berlinstartupjobs
from .web3 import scrape_web3career
from .wwr import scrape_weworkremotely

def scrape_all(term: str):
    sources = []
    b_url, b = scrape_berlinstartupjobs(term)
    w3_url, w3 = scrape_web3career(term)
    wwr_url, wwr = scrape_weworkremotely(term)

    sources = [
        ("berlinstartupjobs.com", b_url, b),
        ("web3.career", w3_url, w3),
        ("weworkremotely.com", wwr_url, wwr),
    ]

    # 합치기(원하면 source별로 그룹핑해서 템플릿에 전달해도 됨)
    merged = b + w3 + wwr
    return sources, merged