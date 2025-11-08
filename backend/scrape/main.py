from scrape import scrape_web, split_dom_content, clean_body_content, extract_body_content

if __name__ == "__main__":
    result = scrape_web("https://portfolio-web-nu-six.vercel.app/")
    body_content = extract_body_content(result)
    cleaned_body_content = clean_body_content(body_content)
    print(cleaned_body_content)
    
