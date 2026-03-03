# Write a python program that takes a URL on the command line, fetches the page, and outputs (one per line)
#       1. Page Title (without any HTML tags)
#       2. Page Body (just the text, without any html tags)
#       3. All the URLs that the page points/links to


import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def fetch_page_text(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def create_soup(url):
    page = fetch_page_text(url)
    return BeautifulSoup(page, "lxml")


def get_title(soup):
    if(soup.title and soup.title.string):
        title = soup.title.string.strip()
    else:
        title = "Title not available for this website"
    return title


def get_body(soup):
    if(soup.body):
        body = soup.body.get_text(separator=" ", strip=True)
    else:
        body = "Body of website not available"
    return body


def build_full_links(base_url, link):
    if(link.startswith("http://") or link.startswith("https://") or link.startswith("tel:") or link.startswith("mailto:")):
        return link
    if(base_url.endswith("/")):
        base_url = base_url[:-1]
    if(link.startswith("/")):
        return base_url + link
    return base_url + "/" + link


def get_links(soup, base_url):
    links = set()
    for tag in soup.find_all("a", href=True):
        link = tag["href"]

        if(link.startswith("#")):
            continue

        full_url = build_full_links(base_url, link)
        links.add(full_url)

    return links


def main():
    if(len(sys.argv) != 2):
        print("Use: python scraper.py https://example.com")
        sys.exit(1)

    url = sys.argv[1]

    if(not url.startswith("https")):
        url = "https://"+url

    soup = create_soup(url)

    print("Title:")
    print(get_title(soup))

    print("Body:")
    print(get_body(soup))

    print("Links:")
    links = get_links(soup, url)
    for link in links:
        print(link)


if __name__ == "__main__":
    main()