import csv
import pprint
import time

import bs4 as bs4
import requests

company_info = []


def scrape_vertical_market(url):
    global company_info

    print(f"Scraping: {url}")
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")

    res = soup.find("div", class_="et_pb_section et_pb_section_2 et_section_regular")
    children = res.findChildren("div", recursive=False)
    for child in children:
        # This section has the information about the company
        if "et_pb_with_border" in child.get("class"):
            res = child.find_all("div", class_="et_pb_text_inner")
            name_and_year = res[0].text.strip().split("\n")
            company_name = name_and_year[0]
            acquired_year = ""
            if len(name_and_year) > 1:
                acquired_year = name_and_year[1]

            # Try to find description
            company_description = ""
            if res[1].find("p"):
                company_description = res[1].find("p").text

            # Try to find link
            company_link = ""
            if res[1].find("a"):
                company_link = res[1].find("a").get("href")

            # print(f"Company: {company_name}, Acquired: {acquired_year}")
            # print(f"text: {company_description}, link: {company_link} \n\n")

            company_info.append(
                {
                    "company_name": company_name,
                    "acquired_year": acquired_year,
                    "description": company_description,
                    "link": company_link,
                }
            )


def main():
    print("Begin scrape")
    url = "https://jonassoftware.com/our-companies"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")

    links = []
    for link in soup.find_all("a"):
        if "vertical-market" in link.get("href"):
            links.append(link.get("href"))
    for link in links:
        scrape_vertical_market(url=link)
        time.sleep(0.1)

    pprint.pprint(company_info)

    # field names
    fields = ["company_name", "acquired_year", "description", "link"]

    # name of csv file
    filename = "temp.csv"

    # writing to csv file
    with open(filename, "w") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(company_info)


if __name__ == "__main__":
    main()
