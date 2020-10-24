from scrapper import scrapWEWORKREMOTELY, scrapSTACKOVERFLOW, scrapREMOTEOK
from flask import Flask, render_template, request, redirect, send_file
from exporter import save_to_file

db = {}

app = Flask("Dev Job Finder")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result")
def result():
    try:
        title_list = []
        company_list = []
        apply_list = []

        searchKeyword = request.args.get('search')
        searchKeyword = searchKeyword.lower()

        if db.get(searchKeyword):
            title_list = db[searchKeyword][0]
            company_list = db[searchKeyword][1]
            apply_list = db[searchKeyword][2]
        else:
            STACKOVERFLOW = scrapSTACKOVERFLOW(searchKeyword)
            REMOTEOK = scrapREMOTEOK(searchKeyword)
            WEWORKREMOTELY = scrapWEWORKREMOTELY(searchKeyword)

            for company, title, link in zip(STACKOVERFLOW[0], STACKOVERFLOW[1], STACKOVERFLOW[2]):
                title_list.append(title)
                company_list.append(company)
                apply_list.append(link)

            for company, title, link in zip(REMOTEOK[0], REMOTEOK[1], REMOTEOK[2]):
                title_list.append(title)
                company_list.append(company)
                apply_list.append(link)

            for company, title, link in zip(WEWORKREMOTELY[0], WEWORKREMOTELY[1], WEWORKREMOTELY[2]):
                title_list.append(title)
                company_list.append(company)
                apply_list.append(link)

            db[searchKeyword] = title_list, company_list, apply_list
    except Exception as e:
        print(f"런타임 에러 발생!! : {e}")
        return redirect("/")

    return render_template("result.html", keyword=searchKeyword, company=company_list, title=title_list, apply=apply_list, len=len, zip=zip)


@ app.route("/export")
def export():
    try:
        keyword = request.args.get('search')
        keyword = keyword.lower()
        if not keyword:
            raise Exception()

        jobs = db.get(keyword)
        if not jobs:
            raise Exception()
        save_to_file(jobs, keyword)
        return send_file(f"csv/{keyword}_jobs.csv", mimetype="text/csv", attachment_filename=f"{keyword}_jobs.csv", as_attachment=True)
    except Exception as e:
        print(f"런타임 에러 발생!! : {e}")
        return redirect("/")


app.run()
