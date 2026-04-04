import sys
import os

# Setup paths
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from collecters.company_discovery import get_companies
from collecters.people_generator import get_people_roles
from engines.role_email_generator import generate_role_emails
from engines.email_verify import verify_email_domain
import pandas as pd

def main():
    print("🚀 Starting Scraper...")
    companies = get_companies()
    results = []

    for name, domain in companies[:5]: # Limit to 5 for testing
        print(f"🏢 Checking: {name}")
        people = get_people_roles(name)
        
        for person in people:
            emails = generate_role_emails(domain, person['role'])
            for email in emails:
                if verify_email_domain(email):
                    print(f"   ✅ Found: {email}")
                    results.append({"Company": name, "Name": f"{person['first_name']} {person['last_name']}", "Email": email})

    df = pd.DataFrame(results)
    df.to_csv("final_contacts.csv", index=False)
    print("🏁 DONE! Check final_contacts.csv")

if __name__ == "__main__":
    main()