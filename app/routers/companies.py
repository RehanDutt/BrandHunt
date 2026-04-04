from fastapi import APIRouter
import sys
import os

# Fix paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from collecters.company_discovery import get_companies
from collecters.people_generator import get_people_roles
from engines.role_email_generator import generate_role_emails
from engines.email_verify import verify_email_domain

router = APIRouter()

@router.get("/companies")
def run_sponsorship_discovery():
    print("🚀 DISCOVERY STARTED")
    
    # 1. Get companies from your scraper
    scraped_companies = get_companies()
    
    # 2. RESUME DEMO MODE: High-value Indian D2C startups
    # We use a list of dictionaries to stay consistent with your logic
    test_list = [
        ("Rebel Foods", "rebelfoods.com"),
        ("Boat Lifestyle", "boat-lifestyle.com"),
        ("Lenskart", "lenskart.com")
    ]
    
    # Combine lists
    companies_to_process = test_list + scraped_companies
    final_results = []

    # 3. Process the top 3 (Rebel Foods, Boat, Lenskart)
    for company_name, domain in companies_to_process[:3]:
        print(f"🔍 Processing: {company_name} (Domain: {domain})")
        
        # Call the Gemini generator
        people = get_people_roles(company_name)
        print(f"✅ Found {len(people)} people for {company_name}")
        
        for person in people:
            first = person.get('first_name', 'Team')
            last = person.get('last_name', '')
            role = person.get('role', 'Marketing')
            
            # --- EMAIL GENERATION & VERIFICATION ---
            # We try to verify, but we keep the lead even if verification is 'unsure'
            emails = generate_role_emails(domain, role)
            best_email = f"{first.lower()}@{domain}" # Default fallback email
            
            for email in emails:
                if verify_email_domain(email):
                    print(f"   ✨ Verified: {email}")
                    best_email = email
                    break 

            # 4. ADD TO FINAL RESULTS (The Bucket)
            # We move this OUTSIDE the verification check so you always get data
            final_results.append({
                "company": company_name,
                "name": f"{first} {last}".strip(),
                "email": best_email,
                "role": role,
                "status": "Verified" if best_email in emails else "Estimated"
            })
    
    print(f"🏁 DONE! Total contacts found: {len(final_results)}")
    
    return {
        "status": "success",
        "count": len(final_results),
        "data": final_results
    }