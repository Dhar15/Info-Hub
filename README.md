# 📚 Info Hub

**Info Hub** is your daily dose of curated knowledge — all in one place. This intelligent info aggregator fetches and displays:

- 📰 **News of the Day** — Top stories scraped from Inshorts  
- 📜 **On This Day in History** — Significant historical events via Wikipedia  
- 🗣️ **Word of the Day** — Vocabulary building via dictionary APIs or scraping  
- 📘 **Financial Term of the Day** — Pulled directly from a Gmail account (Investopedia newsletter) using the Gmail API

---

## 🚀 Live Demo
🔗 [Visit the Live App](https://infohub-186959239227.asia-south1.run.app/)

---

## 🧩 Features

| Feature                  | Source                                 |
|--------------------------|----------------------------------------|
| News Headlines           | Inshorts API scraping                  |
| Today in History         | Wikipedia                              |
| Word of the Day          | Merriam-Webster or alternate sources   |
| Financial Term of the Day | Gmail API – Fetches from Investopedia |

---

## 🛠️ Tech Stack

- `Flask` (Python Web Framework)
- `Gmail API` (OAuth 2.0 + Google API Client)
- `BeautifulSoup` (for web scraping)
- `Cloud Run` (for deployment)

---

## 🧪 Local Setup

### 🔗 Clone the Repo

```bash
git clone https://github.com/Dhar15/Info-Hub.git
cd Info-Hub
pip install -r requirements.txt
python app.py
