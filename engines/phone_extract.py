import re
import phonenumbers


def extract_phone_numbers(text, country="IN"):
    """
    Extracts and validates phone numbers from raw text.
    Returns a list of E.164 formatted phone numbers.
    """
    found_numbers = set()

    # loose regex to catch phone-like patterns
    candidates = re.findall(r'(\+?\d[\d\s\-\(\)]{8,15})', text)

    for candidate in candidates:
        try:
            parsed = phonenumbers.parse(candidate, country)
            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164
                )
                found_numbers.add(formatted)
        except Exception:
            continue

    return list(found_numbers)
