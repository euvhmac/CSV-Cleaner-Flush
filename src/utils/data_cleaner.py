import phonenumbers
import pandas as pd

VALID_DDD = {
    11, 12, 13, 14, 15, 16, 17, 18, 19,
    21, 22, 24,
    27, 28,
    31, 32, 33, 34, 35, 37, 38,
    41, 42, 43, 44, 45, 46,
    47, 48, 49,
    51, 53, 54, 55,
    61,
    62, 64,
    63,
    65, 66,
    67,
    68,
    69,
    71, 73, 74, 75, 77,
    79,
    81, 87,
    82,
    83,
    84,
    85, 88,
    86, 89,
    91, 93, 94,
    92, 97,
    95,
    96,
    98, 99
}

def validate_and_format_phone(phone, region="BR"):
    """
    Valida e formata um número de telefone brasileiro. Números devem ter 11 dígitos no formato <DDD><9><número>.
    """
    try:
        phone = phone.strip()
        if len(phone) != 11 or not phone.isdigit():
            return None

        ddd = int(phone[:2])
        if ddd not in VALID_DDD:
            return None

        if phone[2] != "9":
            return None

        phone_with_country_code = f"+55{phone}"
        parsed_phone = phonenumbers.parse(phone_with_country_code, region)
        if phonenumbers.is_valid_number(parsed_phone):
            return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
        else:
            return None
    except phonenumbers.NumberParseException:
        return None

def clean_name(name):
    """
    Padroniza o nome, ajustando a capitalização e removendo espaços extras.
    """
    try:
        return " ".join(word.capitalize() for word in name.strip().split())
    except AttributeError:
        return None

def clean_age(age):
    """
    Garante que a idade seja numérica. Valores inválidos retornam None.
    """
    try:
        age = int(age)
        return age if 0 < age < 120 else None
    except (ValueError, TypeError):
        return None

def clean_gender(gender):
    """
    Padroniza os valores da coluna 'sexo' para 'Masculino' ou 'Feminino'.
    """
    try:
        gender = gender.strip().lower()
        if gender in ["m", "masculino", "male"]:
            return "Masculino"
        elif gender in ["f", "feminino", "female"]:
            return "Feminino"
        else:
            return None
    except AttributeError:
        return None

def clean_source(source):
    """
    Padroniza a origem dos leads, corrigindo capitalização.
    """
    try:
        return source.strip().capitalize() if source.strip() else "Desconhecido"
    except AttributeError:
        return "Desconhecido"

def clean_date(date):
    """
    Converte datas para o formato ISO (YYYY-MM-DD).
    """
    try:
        return pd.to_datetime(date, errors="coerce").strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def remove_leads_without_phone(data):
    """
    Remove leads que não possuem número de telefone válido.
    """
    return data[data["tel"].notnull()]
