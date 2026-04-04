import sys
import os
import requests
import pandas as pd

# ---- FORCE PROJECT ROOT (for VS Code Run) ----
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---- COLLECTORS ----
from collecters.company_discovery import get_companies
from collecters.people_generator import get_people_roles
from collecters.sponsor_pages import get_companies_from_sponsor_pages

# ---- ENGINES ----
from engines.email_patterns import generate_emails
from engines.email_verify import verify_email_domain
from engines.phone_extract import extract_phone_numbers
from engines.role_email_generator import generate_role_emails



def fetch_website_text(domain):
    try:
        response = requests.get(domain, timeout=8)
        return response.text
    except Exception:
        return ""


def main():

    
    SPONSOR_PAGES = [
        "https://moodindigo.org/sponsors",
        "https://techfest.org/sponsors",
        "https://shaastrafest.org/sponsors",
        "https://startupindia.gov.in/content/sih/en/events.html",
    ]

    companies = get_companies()
    print(f"Discovered {len(companies)} companies")

    results = []

    for company_name, domain in companies:
        print(f"Processing company: {company_name}")

        website_text = fetch_website_text(domain)
        phone_numbers = extract_phone_numbers(website_text)

        # 🔹 ROLE GENERATION (unchanged logic)
        roles = get_people_roles(company_name)



        for person in roles:
            first = person["first_name"]
            last = person["last_name"]
            role = person["role"]

            emails = generate_role_emails(domain, role)


            for email in emails:
                if True:
                    results.append({
                        "company": company_name,
                        "role": role,
                        "name": f"{first} {last}",
                        "email": email,
                        "phone": phone_numbers[0] if phone_numbers else "",
                        "verified": True
                    })

    df = pd.DataFrame(results)
    df.drop_duplicates(subset=["email"], inplace=True)
    df.to_csv("verified_sponsorship_contacts.csv", index=False)

    print("\nDONE")
    print(f"Total verified contacts: {len(df)}")
    print("File saved as: verified_sponsorship_contacts.csv")


if __name__ == "__main__":
    main()