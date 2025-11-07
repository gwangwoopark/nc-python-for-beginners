import requests
from bs4 import BeautifulSoup

UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def get_page_soup(url):
    response = requests.get(url, headers={"User-Agent": UserAgent})
    return BeautifulSoup(response.content, "html.parser")


def scrape_berlinstartupjobs(url):
    all_jobs = []

    job_list = get_page_soup(url).find("ul", class_="jobs-list-items")

    if job_list is None:
        return all_jobs

    job_items = job_list.find_all("li")

    for job in job_items:
        job_title = job.find("h4", class_="bjs-jlid__h")
        job_title_text = job_title.text.strip() if job_title else "No title"

        job_link = job_title.find("a").get("href")

        job_company = job.find("a", class_="bjs-jlid__b")
        job_company_text = job_company.text.strip() if job_company else "No company"

        job_description = job.find("div", class_="bjs-jlid__description")
        job_description_text = (
            job_description.text.strip() if job_description else "No description"
        )

        all_jobs.append(
            {
                "title": job_title_text,
                "link": job_link,
                "company": job_company_text,
                "description": job_description_text,
            }
        )

    return all_jobs


def scrape_web3_career(url):
    all_jobs = []

    job_list = get_page_soup(url).find("tbody", class_="tbody")

    if job_list is None:
        return all_jobs

    job_items = job_list.find_all("tr")

    for job in job_items:
        job_title = job.find("h2")
        job_title_text = job_title.text.strip() if job_title else "No title"

        job_link = f"https://web3.career{job.find('div', class_='job-title-mobile').find('a').get('href')}"

        job_company = job.find("td", class_="job-location-mobile").find("h3")
        job_company_text = job_company.text.strip() if job_company else "No company"

        job_categories = job.find_all("span", class_="my-badge")
        job_description_text = " & ".join(
            [category.text.strip() for category in job_categories]
        )

        all_jobs.append(
            {
                "title": job_title_text,
                "link": job_link,
                "company": job_company_text,
                "description": job_description_text,
            }
        )

    return all_jobs


def scrape_weworkremotely(url):
    all_jobs = []

    job_list = get_page_soup(url).find_all("li", class_="new-listing-container")

    if job_list is None:
        return all_jobs

    for job in job_list:
        job_title = job.find("h3", class_="new-listing__header__title")
        job_title_text = job_title.text.strip() if job_title else "No title"

        job_link = f"https://weworkremotely.com{job.find('a', class_='listing-link--unlocked').get('href')}"

        job_company = job.find("p", class_="new-listing__company-name")
        job_company_text = job_company.text.strip() if job_company else "No company"

        job_categories = job.find("div", class_="new-listing__categories").find_all(
            "p", class_="new-listing__categories__category"
        )
        job_description_text = " & ".join(
            [category.text.strip() for category in job_categories]
        )

        all_jobs.append(
            {
                "title": job_title_text,
                "link": job_link,
                "company": job_company_text,
                "description": job_description_text,
            }
        )

    return all_jobs


def scrape_all_jobs(skill_area):
    all_jobs = []
    all_jobs.extend(
        scrape_berlinstartupjobs(
            f"https://berlinstartupjobs.com/skill-areas/{skill_area}/"
        )
    )
    all_jobs.extend(scrape_web3_career(f"https://web3.career/{skill_area}-jobs"))
    all_jobs.extend(
        scrape_weworkremotely(
            f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={skill_area}"
        )
    )
    return all_jobs
