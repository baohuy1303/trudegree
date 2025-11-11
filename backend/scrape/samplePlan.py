import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import re
import os

JSON_FILE = os.path.join(os.path.dirname(__file__), "data", "truman_degree.json")

def scrape_web(website):
    print("Scraping website:", website)

    # Get absolute path to chromedriver.exe (in the same directory as this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_driver_path = os.path.join(current_dir, "chromedriver.exe")
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
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
    return cleaned_body_content

def parsePlan(text):
    # 1. Find program name
    program_match = re.search(r"Home\n(.+)\nThe plan", text)
    program_name = program_match.group(1).strip() if program_match else "Computer Science (BS)"

    # 2. Split semesters
    semesters_raw = re.split(r"(Semester \d)", text)
    semesters = []
    for i in range(1, len(semesters_raw), 2):
        sem_title = semesters_raw[i].strip()
        sem_content = semesters_raw[i+1].strip()
        
        # Extract courses
        course_lines = [line for line in sem_content.split("\n") if line.startswith("-")]
        courses = []
        for line in course_lines:
            # Pattern: "- CODE: Name (X cr)" or "- CODE Name (X cr)"
            match = re.match(r"- ([\w\s/]+(?:\d+|XXX))[:]? (.+?) \((\d+) cr\)", line)
            if match:
                code = match.group(1).strip()
                name = match.group(2).strip()
                credits = int(match.group(3))
                courses.append({"code": code, "name": name, "credits": credits, "note": ""})
            else:
                courses.append({"raw": line.strip()})  # fallback
        
        semesters.append({"semester": sem_title, "courses": courses})

    # 3. Extract elective areas
    electives = {"area_a": [], "area_b": [], "area_c": []}
    for area in ["A", "B", "C"]:
        match = re.search(rf"Area {area} courses\ninclude (.+?)\.", text, re.DOTALL)
        if match:
            courses = [c.strip() for c in match.group(1).split(",")]
            electives[f"area_{area.lower()}"] = courses

    # 4. Extract notes
    notes = re.findall(r"\(\*\*\) = (.+?)\.", text)
    notes += re.findall(r"WE = (.+?)\.", text)
    notes += ["Portfolio required", "Civics Exam recommended in first year"]

    # 5. Create final JSON
    parsed_plan = {
        "program": program_name,
        "semesters": semesters,
        "electives": electives,
        "notes": notes
    }
    with open("samplePlan.json", "w", encoding="utf-8") as f:
        json.dump(parsed_plan, f, indent=2, ensure_ascii=False)


    return parsed_plan


def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]

def scrape_sample_plan(url):
    html = scrape_web(url)
    body_content = extract_body_content(html)
    cleaned_body_content = clean_body_content(body_content)
    return parsePlan(cleaned_body_content)

""" if __name__ == "__main__":
    url = "https://www.truman.edu/fouryearplan/computer-science-bs/"
    html = scrape_web(url)
    body_content = extract_body_content(html)
    cleaned_body_content = clean_body_content(body_content)
    parsePlan(cleaned_body_content) """
