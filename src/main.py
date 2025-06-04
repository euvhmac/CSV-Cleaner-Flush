import pandas as pd
from utils.data_loader import load_data
from utils.data_cleaner import (
    validate_and_format_phone,
    clean_name,
    clean_age,
    clean_gender,
    clean_source,
    clean_date,
    remove_leads_without_phone
)
from utils.email_cleaner import validate_and_normalize_email

def main():
    file_path = "data/raw_data.csv"
    raw_data = load_data(file_path)

    if raw_data is not None:
        print("Carregamento inicial bem-sucedido!")

        print("Validando e formatando números de telefone...")
        raw_data['tel'] = raw_data['tel'].apply(
            lambda x: validate_and_format_phone(str(x)) if pd.notnull(x) else None
        )
        print("Telefones validados com sucesso.")

        print("Removendo leads sem números de telefone...")
        raw_data = remove_leads_without_phone(raw_data)
        print(f"Leads restantes após remoção: {len(raw_data)}")

        print("Validando e normalizando e-mails...")
        for index, email in enumerate(raw_data['email']):
            if pd.notnull(email):
                raw_data.at[index, 'email'] = validate_and_normalize_email(email)
                if index % 500 == 0:
                    print(f"{index} e-mails processados...")
        print("E-mails validados e normalizados.")

        print("Padronizando as colunas restantes...")
        raw_data['name'] = raw_data['name'].apply(clean_name)
        raw_data['firstname'] = raw_data['firstname'].apply(clean_name)
        raw_data['idade'] = raw_data['idade'].apply(clean_age)
        raw_data['sexo'] = raw_data['sexo'].apply(clean_gender)
        raw_data['onde'] = raw_data['onde'].apply(clean_source)
        raw_data['date'] = raw_data['date'].apply(clean_date)
        print("Colunas restantes padronizadas.")

        valid_phones = raw_data['tel'].notnull().sum()
        valid_emails = raw_data['email'].notnull().sum()
        print(f"Telefones válidos: {valid_phones}")
        print(f"E-mails válidos: {valid_emails}")
        print(f"E-mails inválidos: {len(raw_data) - valid_emails}")

        output_file = "data/cleaned_data.csv"
        raw_data.to_csv(output_file, index=False)
        print(f"Dados tratados salvos em: {output_file}")

    else:
        print("Erro ao carregar os dados.")

if __name__ == "__main__":
    main()
