import re
from email_validator import validate_email, EmailNotValidError
from difflib import get_close_matches

KNOWN_DOMAINS = [
    "gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com", "live.com"
]
KNOWN_TLDS = ["com", "org", "net", "edu", "gov", "br"]

def correct_domain(email):
    """
    Corrige o domínio de um e-mail baseado em domínios conhecidos.

    :param email: E-mail como string.
    :return: E-mail com domínio corrigido, ou o original se já for válido.
    """
    try:
        local_part, domain = email.split("@")

        if "." in domain:
            domain_name, tld = domain.rsplit(".", 1)
        else:
            return email

        if tld not in KNOWN_TLDS:
            corrected_tld = get_close_matches(tld, KNOWN_TLDS, n=1, cutoff=0.8)
            tld = corrected_tld[0] if corrected_tld else tld

        corrected_domain = get_close_matches(f"{domain_name}.{tld}", KNOWN_DOMAINS, n=1, cutoff=0.8)
        return f"{local_part}@{corrected_domain[0]}" if corrected_domain else f"{local_part}@{domain_name}.{tld}"
    except Exception:
        return email

def validate_and_normalize_email(email):
    """
    Valida e normaliza um endereço de e-mail, corrigindo pequenos erros.

    :param email: String contendo o e-mail.
    :return: E-mail validado e normalizado ou None se inválido.
    """
    try:
        email = email.strip().lower()

        email = correct_domain(email)

        valid = validate_email(email)
        return valid.email
    except (IndexError, EmailNotValidError):
        return None  # Retornar None se o e-mail não for válido
