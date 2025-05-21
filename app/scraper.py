import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_today_in_history():
    # Automatically get today's month and day
    today = datetime.now()
    month = today.strftime("%B").lower()   # e.g., 'may'
    day = today.strftime("%d").lstrip("0") # e.g., '20'

    url = f"https://www.history.com/this-day-in-history/{month}-{day}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Grab the first <h1> tag (main headline)
    headline_tag = soup.find("h1")

    result = []
    if headline_tag:
        headline = headline_tag.text.strip()
        result.append(f"{headline}")
    else:
        result.append("No headline found.")

    return {"History.com - On This Day": result}

def scrape_word_of_the_day():
    url = "https://www.merriam-webster.com/word-of-the-day"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Get the word
    word_tag = soup.find("h2", class_="word-header-txt")
    word = word_tag.text.strip() if word_tag else "Word not found"

    # Get the meaning (first <p> under wod-definition-container)
    definition_container = soup.find("div", class_="wod-definition-container")
    definition = ""
    if definition_container:
        p_tags = definition_container.find_all("p")
        if p_tags:
            definition = p_tags[0].text.strip()
            example = p_tags[1].text.strip()

    # return {"Merriam Webster - Word of the Day": [f"{word}: {definition}"] if word and definition else ["No word/definition found."]}

    result = []
    if word and definition:
        result.append(f"🗣️ {word}: {definition}")
        if example:
            result.append(f"💬 Example: {example}")
    else:
        result.append("⚠️ No word found today.")

    return {"Merriam Webster - Word of the Day": result}

import requests
from bs4 import BeautifulSoup

def scrape_inshorts_headlines():
    url = "https://m.inshorts.com/en/read"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all span tags with itemprop="headline"
    headlines = soup.find_all("span", itemprop="headline")

    top_headlines = []
    for i, headline in enumerate(headlines[:3]):  # Top 3 only
        text = headline.get_text(strip=True)
        top_headlines.append(f"📰 {i+1}. {text}")

    if not top_headlines:
        top_headlines.append("⚠️ No headlines found today.")

    return {"Inshorts - News of the Day": top_headlines}

def scrape_ibt_term_of_day():
    url = "https://www.ibtimes.com/terms"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    result = []

    term_section = soup.find("div", class_="term-of-day")
    if term_section:
        col_r = term_section.find("div", class_="col-r")
        if col_r:
            h4_tag = col_r.find("h4")
            p_tag = col_r.find("p")

            term = h4_tag.get_text(strip=True) if h4_tag else None
            definition = p_tag.get_text(strip=True).split("Read more")[0] if p_tag else None

            if term and definition:
                result.append(f"📘 {term}: {definition}")
            else:
                result.append("⚠️ Could not extract term or definition.")
        else:
            result.append("⚠️ Section not found.")
    else:
        result.append("⚠️ Term of the Day section not found.")

    return {"IBT - Financial Term of the Day": result}






