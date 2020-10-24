import csv


def save_to_file(jobs, keyword):
    file = open(f"csv/{keyword}_jobs.csv", mode='w', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])
    for title, company, link in zip(jobs[0], jobs[1], jobs[2]):
        writer.writerow([title, company, link])
    return
