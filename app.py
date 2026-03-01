from flask import Flask, render_template, request, redirect, url_for
from scrapers import scrape_all

app = Flask(__name__)

def is_ascii_term(term: str) -> bool:
    # 한글 등 비-ASCII 입력 차단용
    try:
        term.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False

@app.get("/")
def home():
    # error 메시지는 있을 수도/없을 수도
    return render_template("index.html", error=None)

# ✅ 중요: Frozen-Flask가 /go 를 GET으로 때릴 수 있으니 GET도 허용해서 막아줌
@app.get("/go/")
def go_get():
    # 정적 빌드/실수 접근 모두 홈으로
    return redirect(url_for("home"))

@app.post("/go/")
def go():
    term = request.form.get("term", "").strip()

    if not term:
        return render_template("index.html", error="검색어를 입력해주세요.")

    # ✅ 한글 입력 시 안내 메시지
    if not is_ascii_term(term):
        return render_template("index.html", error="영문 키워드로 검색해주세요. (예: python, javascript)")

    # ✅ 정적 빌드-friendly: /search/<term> 로 이동
    return redirect(url_for("search", term=term))

@app.get("/search/<term>/")
def search(term: str):
    term = (term or "").strip()

    # term이 이상하면 홈으로
    if not term:
        return redirect(url_for("home"))

    # 한글이 URL로 들어오는 것도 방지
    if not is_ascii_term(term):
        return render_template("index.html", error="영문 키워드로 검색해주세요. (예: python, javascript)")

    sources, jobs = scrape_all(term)

    # templates/results.html에서 sources도 보여주고 싶으면 같이 넘겨도 됨
    return render_template("results.html", term=term, results=jobs, sources=sources)

if __name__ == "__main__":
    app.run(debug=True)