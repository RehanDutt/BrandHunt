import os
from dotenv import load_dotenv

load_dotenv() # Works locally

# This pulls from the web environment if local .env is missing
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
import requests
import json


def discover_companies_apollo(keyword, count):
    """Improved Google Discovery to find actual company websites."""
    url = "https://google.serper.dev/search"
    # We add -directory -indiamart -linkedin to filter out the junk
    query = f"top {keyword} brands in India official website -directory -indiamart -linkedin -justdial"
    payload = json.dumps({"q": query, "num": 20}) # Ask for more so we can filter down to 'count'
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=payload).json()
        results = response.get('organic', [])
        found = []
        seen_domains = set()

        for r in results:
            link = r.get('link', '')
            domain = link.split('//')[-1].split('/')[0].replace('www.', '')
            
            if any(x in domain for x in ['google', 'facebook', 'instagram', 'youtube', 'wikipedia']):
                continue
            if domain in seen_domains:
                continue
                
            # --- REPLACE FROM HERE ---
            # 1. Get the raw title from the search result
            raw_name = r.get('title', 'Unknown').split(':')[0].split('-')[0].split('|')[0].strip()
            
            # 2. Check if the title is junk like "Home" or "Our Brands"
            junk_words = ["home", "brands", "official", "welcome", "website", "india"]
            if any(word in raw_name.lower() for word in junk_words) or len(raw_name) < 3:
                # Use the website domain (e.g., 'coolberg') if the title is generic
                clean_name = domain.split('.')[0].capitalize()
            else:
                # Use the first 3 words of the title
                clean_name = ' '.join(raw_name.split()[:3])
            # --- TO HERE ---
            
            found.append((clean_name, domain))
            seen_domains.add(domain)
            
            if len(found) >= count:
                break
        return found
    except Exception as e:
        print(f"Search Error: {e}")
        return []

def get_people_roles(company_name, domain):
    """Enhanced search to find real names and verify patterns."""
    search_url = "https://google.serper.dev/search"
    # Searching for a specific human name via LinkedIn
    query = f"site:linkedin.com/in/ '{company_name}' Marketing Manager India"
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    
    try:
        search_res = requests.post(search_url, headers=headers, json={"q": query}).json()
        top_result = search_res.get('organic', [{}])[0].get('title', "")
        
        # Extracting name from Title like "Arjun Sharma - Marketing Head - Amul"
        full_name = top_result.split('-')[0].split('|')[0].strip()
        parts = full_name.split()
        first = parts[0] if parts else "Contact"
        last = parts[1] if len(parts) > 1 else ""

        # Hit Hunter.io
        hunter_url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first}&last_name={last}&api_key={HUNTER_API_KEY}"
        h_res = requests.get(hunter_url).json()
        h_data = h_res.get('data', {})

        if h_data and h_data.get('email'):
            return {
                "first_name": first, "last_name": last,
                "role": "Marketing Leadership",
                "email": h_data.get('email'),
                "status": "✅ Verified (Hunter.io)"
            }
        
        # If Hunter fails, we use a more professional Pattern Match
        # Most Indian corporates use {first}.{last} or {first}
        return {
            "first_name": first, "last_name": last,
            "role": "Marketing Dept",
            "email": f"{first.lower()}@{domain}",
            "status": "🎯 Pattern Match"
        }
    except:
        return None