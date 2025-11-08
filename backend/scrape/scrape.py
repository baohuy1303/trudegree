import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import re


JSON_FILE = "truman_degree.json"

def scrape_web(website):
    print("Scraping website:", website)

    chrome_driver_path = "./chromedriver.exe"
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Website opened successfully")

        # Wait a bit to allow JS to load events (Truman’s page uses JavaScript)
        time.sleep(10)

        html = driver.page_source
        return html

    except Exception as e:
        print("Error opening website:", e)
        return None

    finally:
        driver.quit()


def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    if body is None:
        return None
    return str(body)

def get_block(section_name):
    pattern = rf"{section_name}\n(.*?)\n[A-Z][^\n]+(?:\n|$)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    # Remove scripts, styles, and other irrelevant tags
    for tag in soup(['script', 'style', 'noscript']):
        tag.extract()

    cleaned_body_content = soup.get_text(separator="\n")
    cleaned_body_content = "\n".join(
        line.strip() for line in cleaned_body_content.splitlines() if line.strip()
    )
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_body_content, f, indent=2, ensure_ascii=False)
    return cleaned_body_content


def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]

def scrape_sample_plan(url):
    html = scrape_web(url)
    body_content = extract_body_content(html)
    cleaned_body_content = clean_body_content(body_content)
    return cleaned_body_content
    
if __name__ == "__main__":
    url = "https://www.truman.edu/fouryearplan/computer-science-bs/"
    html = scrape_web(url)
    body_content = extract_body_content(html)
    cleaned_body_content = clean_body_content(body_content)
