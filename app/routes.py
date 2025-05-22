from flask import Blueprint, render_template
from .scraper import scrape_today_in_history, scrape_word_of_the_day, scrape_inshorts_headlines, scrape_financial_term_of_day
from datetime import datetime

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route("/")
def home():
    history_data = scrape_today_in_history()
    word_data = scrape_word_of_the_day()
    news_data = scrape_inshorts_headlines()
    fin_data = scrape_financial_term_of_day()

    # Merge both into one dictionary
    all_data = {**history_data, **word_data, **news_data, **fin_data}

    today = datetime.now().strftime("%B %d, %Y")

    return render_template("index.html", data=all_data, today=today)