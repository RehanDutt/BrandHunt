import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SEED_PAGES = [
    "https://inc42.com/startups/",
    "https://yourstory.com/companies",
    "https://www.startupindia.gov.in/content/sih/en/search.html?industries=D2C",
]

# words that clearly indicate NON-companies
NAME_BLACKLIST = [
    "login", "sign", "request", "proposal", "advertise", "career",
    "job", "podcast", "blog", "article", "news", "view",
    "guest", "spotlight", "press", "media", "summit",
]

# domains we NEVER want (directory sites themselves)
DOMAIN_BLACKLIST = [
    "inc42.com",
    "yourstory.com",
    "startupindia.gov.in",
]

def clean_domain(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
    except:
        pass
    return None


def is_valid_company(name, domain):
    lname = name.lower()

    if len(name) < 3:
        return False

    for bad in NAME_BLACKLIST:
        if bad in lname:
            return False

    for bad_domain in DOMAIN_BLACKLIST:
        if bad_domain in domain:
            return False

    return True


def get_companies(limit=30):
    """
    Returns CLEAN list of (company_name, domain)
    Keeps brands + event brands
    Removes nav / blog / CTA garbage
    """

    companies = {}

    for page in SEED_PAGES:
        print(f"Crawling directory: {page}")

        try:
            res = requests.get(page, headers=HEADERS, timeout=12)
            soup = BeautifulSoup(res.text, "html.parser")

            for a in soup.find_all("a", href=True):
                name = a.get_text(strip=True)
                href = a["href"].strip()

                if not name:
                    continue

                full_url = urljoin(page, href)
                domain = clean_domain(full_url)

                if not domain:
                    continue

                if not is_valid_company(name, domain):
                    continue

                companies[domain] = name

                if len(companies) >= limit:
                    break

            time.sleep(2)

        except Exception as e:
            print("Directory crawl failed:", e)

        if len(companies) >= limit:
            break

    return [(name, domain) for domain, name in companies.items()]
