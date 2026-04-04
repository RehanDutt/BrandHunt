def generate_emails(first_name, last_name, domain):
    first = first_name.lower().strip()
    last = last_name.lower().strip()
    fi = first[0]

    emails = [
        f"{first}@{domain}",
        f"{first}.{last}@{domain}",
        f"{fi}{last}@{domain}",
        f"{first}{last}@{domain}"
    ]

    return list(set(emails))

