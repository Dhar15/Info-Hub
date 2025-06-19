import requests
from bs4 import BeautifulSoup
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import base64
import re
import html

# Load env vars
load_dotenv()

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
    for i, headline in enumerate(headlines[:5]):  # Top 3 only
        text = headline.get_text(strip=True)
        top_headlines.append(f"📰 {i+1}. {text}")

    if not top_headlines:
        top_headlines.append("⚠️ No headlines found today.")

    return {"Inshorts - News of the Day": top_headlines}

############ GMAIL API INTEGRATION ############

def get_gmail_service():
    creds = Credentials(
        None,
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        token_uri=os.getenv("GMAIL_TOKEN_URI"),
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET")
    )
    
    # Refresh the token if needed
    if creds.expired or not creds.valid:
        creds.refresh(Request())

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_financial_term_email(service):
    result = service.users().messages().list(
        userId=os.getenv("GMAIL_USER_EMAIL", "me"),
        q='from:newsletters@mail.investopedia.com subject:"Term of the Day:"',
        maxResults=1
    ).execute()

    print("Result",result)

    messages = result.get('messages', [])
    print("Messages",messages)
    if not messages:
        return "⚠️ No Term of the Day email found."

    msg = service.users().messages().get(userId='me',id=messages[0]['id'],format='metadata',metadataHeaders=['Subject']).execute()
    print("Msg:",msg)

   # Extract subject line
    subject = next((h['value'] for h in msg['payload'].get('headers', []) if h['name'] == 'Subject'), "Unknown Term")
    subject_match = re.search(r'Term of the Day: (.+)', subject)
    term = subject_match.group(1).strip() if subject_match else "Unknown Term"
    print("Subject",subject)
    print("Subject_match",subject_match)
    print("Term",term)

    # Use the snippet as the definition
    raw_snippet = msg.get('snippet', '')
    definition = html.unescape(raw_snippet.strip())

    print("Snippet",raw_snippet)
    print("Definition",definition)

    return f"📘 {term}: {definition}"

def scrape_financial_term_of_day():
    try:
        service = get_gmail_service()
        term_of_day = get_financial_term_email(service)
        return {"Investopedia - Financial Term of the Day": [term_of_day]}
    except Exception as e:
        return {"Investopedia - Financial Term of the Day": [f"⚠️ Error: {str(e)}"]}