import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import re
import schedule
import time
from telegram import Bot

# Download NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')

# Telegram config - replace these
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
TELEGRAM_CHANNEL_ID = '@yourchannelusername'  # or numeric ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Common IT technical skills keywords for matching
TECH_SKILLS = [
    'python', 'java', 'c++', 'javascript', 'sql', 'aws', 'azure', 'docker', 'kubernetes',
    'linux', 'git', 'react', 'angular', 'node.js', 'machine learning', 'data analysis',
    'devops', 'agile', 'scrum', 'microservices', 'rest api', 'html', 'css', 'cloud',
    'spring', 'hibernate', 'nosql', 'mongodb', 'tensorflow', 'pytorch', 'big data',
    'spark', 'hadoop', 'salesforce', 'sap', 'oracle', 'jira', 'jenkins'
]

STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

def extract_keywords(text, num_keywords=5):
    text = clean_text(text)
    words = word_tokenize(text)
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    freq = Counter(words)
    common = freq.most_common(num_keywords)
    return [word for word, count in common]

def extract_tech_skills(text, num_skills=5):
    text = clean_text(text)
    found_skills = [skill for skill in TECH_SKILLS if skill in text]
    return found_skills[:num_skills]

# --- Scraper for TCS (https://www.tcs.com/careers) ---
def scrape_tcs():
    url = "https://www.tcs.com/careers"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # TCS careers page is mostly JS, but they have a "Search Jobs" link:
        # We'll scrape https://www.tcs.com/careers/careers-home/jobs
        jobs_url = "https://www.tcs.com/careers/careers-home/jobs"
        r2 = requests.get(jobs_url, timeout=10)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        # Jobs are loaded dynamically, so fallback to empty
        # For demo, return empty list
        return []
    except Exception as e:
        print(f"TCS scrape error: {e}")
        return []

# --- Scraper for Infosys (https://www.infosys.com/careers.html) ---
def scrape_infosys():
    # Infosys uses dynamic content, but they have a job search API:
    # For demo, return empty list
    return []

# --- Scraper for Wipro (https://careers.wipro.com/) ---
def scrape_wipro():
    # Wipro jobs are dynamic, no static HTML jobs list
    return []

# --- Scraper for HCL (https://www.hcltech.com/careers) ---
def scrape_hcl():
    # HCL careers page is dynamic, no static jobs list
    return []

# --- Scraper for Tech Mahindra (https://careers.techmahindra.com/) ---
def scrape_techmahindra():
    # Tech Mahindra jobs page is dynamic, no static jobs list
    return []

# --- Scraper for LTI (https://careers.lntinfotech.com/) ---
def scrape_lti():
    url = "https://careers.lntinfotech.com/job-search-results"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # The page is dynamic, no static jobs
        return []
    except Exception as e:
        print(f"LTI scrape error: {e}")
        return []

# --- Scraper for Mindtree (https://www.mindtree.com/careers) ---
def scrape_mindtree():
    # Mindtree careers page is dynamic
    return []

# --- Scraper for Persistent Systems (https://www.persistent.com/careers/) ---
def scrape_persistent():
    url = "https://www.persistent.com/careers/"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # No static job listings found
        return []
    except Exception as e:
        print(f"Persistent scrape error: {e}")
        return []

# --- Scraper for Hexaware (https://hexaware.com/careers/) ---
def scrape_hexaware():
    url = "https://hexaware.com/careers/"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        # No static job listings found
        return []
    except Exception as e:
        print(f"Hexaware scrape error: {e}")
        return []

# --- Example scraper for a company with static job listings ---
def scrape_example_static():
    # This is a placeholder for companies with static job listings
    # For demo, return empty list
    return []

# Combine all scrapers here
def scrape_all_companies():
    all_jobs = []
    # Call each scraper and extend all_jobs
    all_jobs.extend(scrape_tcs())
    all_jobs.extend(scrape_infosys())
    all_jobs.extend(scrape_wipro())
    all_jobs.extend(scrape_hcl())
    all_jobs.extend(scrape_techmahindra())
    all_jobs.extend(scrape_lti())
    all_jobs.extend(scrape_mindtree())
    all_jobs.extend(scrape_persistent())
    all_jobs.extend(scrape_hexaware())
    # Add more scrapers here as you implement them
    return all_jobs

def format_jobs_table(jobs):
    if not jobs:
        return "No new jobs found today."
    headers = ["Company", "Title", "Location", "Link", "Keywords", "Tech Skills"]
    table = []
    for job in jobs:
        table.append([
            job.get("Company", ""),
            job.get("Title", ""),
            job.get("Location", ""),
            job.get("Link", ""),
            job.get("Keywords", ""),
            job.get("Tech Skills", "")
        ])
    return tabulate(table, headers, tablefmt="github")

def send_to_telegram(message):
    max_len = 4000
    for i in range(0, len(message), max_len):
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message[i:i+max_len], parse_mode='Markdown')

def job_scraper_job():
    print("Scraping jobs from company career pages...")
    jobs = scrape_all_companies()
    if not jobs:
        print("No jobs found.")
        send_to_telegram("No new IT jobs found today from company career pages.")
        return

    message = "*Daily IT Jobs Update from Company Career Pages*\n\n"
    message += format_jobs_table(jobs)
    send_to_telegram(message)
    print("Jobs sent to Telegram.")

if __name__ == "__main__":
    # Run once immediately
    job_scraper_job()

    # Schedule daily at 9 AM
    schedule.every().day.at("09:00").do(job_scraper_job)

    print("Scheduler started. Waiting for next run...")
    while True:
        schedule.run_pending()
        time.sleep(60)
