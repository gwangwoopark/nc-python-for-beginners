from flask import Flask, redirect, render_template, request, url_for
from scraper import scrape_all_jobs

app = Flask("__name__")

@app.route("/")
def home():
    return render_template("home.html")

# path parameter 방식 (freeze용 - 정적 파일 생성에 적합)
@app.route("/search/<keyword>")
def search(keyword):
    jobs = scrape_all_jobs(keyword)
    return render_template("search.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
