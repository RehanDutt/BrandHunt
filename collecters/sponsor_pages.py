import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SponsorshipBot/1.0)"
}

def extract_domain(url):
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except:
        return None

def get_companies_from_sponsor_pages(pages):
    companies = set()

    for page_url in pages:
        try:
            res = requests.get(page_url, headers=HEADERS, timeout=10)
            if res.status_code != 200:
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            # find all links (sponsors usually linked)
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                text = a.get_text(strip=True)

                # skip junk
                if not text or len(text) < 2:
                    continue
                if any(x in href.lower() for x in ["facebook", "instagram", "linkedin", "twitter"]):
                    continue

                # absolute URL
                full_url = urljoin(page_url, href)
                domain = extract_domain(full_url)

                if domain and "." in domain:
                    clean_name = re.sub(r"[^A-Za-z0-9 &]", "", text)
                    if len(clean_name) >= 2:
                        companies.add((clean_name, domain))

        except Exception:
            continue

    return list(companies)
