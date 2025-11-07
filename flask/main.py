from flask import Flask, redirect, render_template, request, url_for

app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template("home.html", name="Gwangwoo")

db = {}

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect(url_for("home"))
    else:
        jobs = []
        return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect(url_for("home"))
    if keyword is not db:
      return redirect(url_for("search", keyword=keyword))
    else:
        jobs = []
        return render_template("export.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
