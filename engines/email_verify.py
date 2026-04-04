import dns.resolver


def verify_email_domain(email):
    """
    Returns True if the email domain has MX records.
    """
    try:
        domain = email.split("@")[1]
        dns.resolver.resolve(domain, "MX")
        return True
    except Exception:
        return False
