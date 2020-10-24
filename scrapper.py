import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}


def scrapREMOTEOK(keyword):
    company_list = []
    title_list = []
    apply_list = []

    url = f"https://remoteok.io/remote-dev+{keyword}-jobs"

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    company = soup.find_all("h3", {"itemprop": "name"})
    for item in company:
        company_list.append(item.get_text())

    title = soup.find_all("h2", {"itemprop": "title"})
    for item in title:
        title_list.append(item.get_text())

    apply = soup.find_all("a", {"itemprop": "url"})
    for item in apply:
        link = f"https://remoteok.io{item.get('href')}"
        apply_list.append(link)

    return company_list, title_list, apply_list


def scrapSTACKOVERFLOW(keyword):
    company_list = []
    title_list = []
    apply_list = []

    url = f"https://stackoverflow.com/jobs?r=true&q={keyword}"

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    company = soup.find_all("h3", {"class": "fc-black-700 fs-body1 mb4"})
    for item in company:
        company_name = item.find("span")
        company_list.append(company_name.get_text().strip())

    items = soup.find_all("a", {"class": "s-link stretched-link"})
    for item in items:
        title_list.append(item.get_text())
        apply_list.append(f"https://stackoverflow.com{item.get('href')}")

    return company_list, title_list, apply_list


def scrapWEWORKREMOTELY(keyword):
    company_list = []
    title_list = []
    apply_list = []

    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    section = soup.find_all("section", {"class": "jobs"})
    for item in section:
        a = item.select("li > a")
        for item2 in a:
            if str(item2.parent['class']) != "['view-all']":
                link = f"https://weworkremotely.com{item2.get('href')}"
                apply_list.append(link)

                company = item2.find("span", {"class": "company"})
                company_list.append(company.get_text())

                title = item2.find("span", {"class": "title"})
                title_list.append(title.get_text())
            else:
                continue

    return company_list, title_list, apply_list
