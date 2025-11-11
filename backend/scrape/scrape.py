import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import os

JSON_FILE = os.path.join(os.path.dirname(__file__), "data", "truman_REQ.json")

def scrape_web(website):
    print("Scraping website:", website)

    chrome_driver_path = "./chromedriver.exe"
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("✅ Website opened successfully")
        print("➡️ Log in manually, navigate to your target page.")
        input("Press ENTER once you're ready to start scraping manually...")

        all_pages = []
        page_num = 1

        while True:
            command = input("\nPress ENTER to scrape this page, or type 'q' to quit: ").strip().lower()
            if command == "q":
                print("🛑 Ending session.")
                break

            print(f"📸 Scraping page {page_num}...")
            html = driver.page_source
            extracted = extract_target_div(html)
            if extracted:
                all_pages.append({
                    "page_number": page_num,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "content": extracted
                })
                save_json(all_pages)
                print(f"✅ Page {page_num} saved to {JSON_FILE}")
            else:
                print("⚠️ Target div not found on this page.")

            page_num += 1
            print("➡️ Click next arrow in the browser, wait for it to load, then press ENTER again.")

        return all_pages

    except Exception as e:
        print("❌ Error during scraping:", e)
        return []

    finally:
        driver.quit()
        print("🔒 Browser closed.")


def extract_target_div(html):
    """Extract only the target div's text content."""
    soup = BeautifulSoup(html, 'html.parser')
    parent_div = soup.find("div", id="plan-card")
    first_child_div = parent_div.find("div", recursive=False)
    if not first_child_div:
        return None

    # Second child of first_child_div
    children_of_first = first_child_div.find_all(recursive=False)
    second_child_of_first = children_of_first[1] if len(children_of_first) > 1 else None
    if not second_child_of_first:
        return None

    # Second child of second_child_of_first
    children_of_second = second_child_of_first.find_all(recursive=False)
    second_child_of_second = children_of_second[1] if len(children_of_second) > 1 else None
    if not second_child_of_second:
        return None

    # Clean up: remove unwanted nested tags
    for tag in second_child_of_second(['script', 'style', 'noscript']):
        tag.decompose()

    text = second_child_of_second.get_text(separator="\n")
    cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return cleaned


def save_json(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    url = "https://mercury15.truman.edu:8474/"
    scrape_web(url)
