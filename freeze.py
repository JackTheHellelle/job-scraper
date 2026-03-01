from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

# GitHub Pages(프로젝트 페이지)에서는 상대경로 링크가 편함
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_DESTINATION"] = "dist"

# 정적 빌드 시 만들 term 목록(예시)
TERMS = ["python", "javascript", "java", "react", "next.js", "flutter"]

@freezer.register_generator
def search():
    for term in TERMS:
        yield {"term": term}

if __name__ == "__main__":
    freezer.freeze()