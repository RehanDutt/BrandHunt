# engines/role_email_generator.py

ROLE_EMAIL_MAP = {
    "Partnerships": ["partnerships", "alliances", "collaborations"],
    "Brand": ["brand", "branding"],
    "Marketing": ["marketing", "growth"],
    "Sponsorships": ["sponsorships", "partners"],
}


def generate_role_emails(domain, role):
    """
    Generates high-intent, role-based emails for sponsorship outreach
    Returns list of emails
    """

    emails = []

    if not domain:
        return emails

    domain = domain.replace("https://", "").replace("http://", "").strip("/")

    prefixes = ROLE_EMAIL_MAP.get(role, [])

    for prefix in prefixes:
        emails.append(f"{prefix}@{domain}")

    return emails
