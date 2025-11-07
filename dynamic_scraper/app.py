from playwright.sync_api import sync_playwright
import time 
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

time.sleep(5)

# page.goto("https://www.wanted.co.kr/jobsfeed")

# time.sleep(5)

# page.click("button.Aside_searchButton__Ib5Dn")

# time.sleep(5)

# page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

# time.sleep(5)

# page.keyboard.down("Enter")

# time.sleep(5)

# page.click("a#search_tab_position")

# time.sleep(5)

for i in range(5):
  page.keyboard.down("End")
  time.sleep(5)

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

jobs_db = []

for job in jobs:
  link = f"https://www.wanted.co.kr{job.find('a')['href']}"
  title = job.find("strong", class_="JobCard_title___kfvj").text
  company_name = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu").text
  required_experience = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l").text
  reward = job.find("span", class_="JobCard_reward__oCSIQ").text
  job = {
    "link": link,
    "title": title,
    "company_name": company_name,
    "required_experience": required_experience,
    "reward": reward
  }
  jobs_db.append(job)

print(jobs_db)

file = open("jobs.csv", "w")

writter = csv.writer(file)

writter.writerow(jobs_db[0].keys())

for job in jobs_db:
  writter.writerow(job.values())

file.close()