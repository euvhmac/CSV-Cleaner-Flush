import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from utils.data_cleaner import (
    validate_and_format_phone,
    clean_name,
    clean_age,
    clean_gender,
    clean_source,
    clean_date,
)
from utils.email_cleaner import validate_and_normalize_email

plt.style.use("dark_background")
sns.set_palette("coolwarm")
st.set_page_config(
    page_title="CSV Cleaner - Flush",
    page_icon="assets/favicon.ico",
)


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

def process_csv(file):
    data = pd.read_csv(file)

    data["tel"] = data["tel"].apply(
        lambda x: validate_and_format_phone(str(x)) if pd.notnull(x) else None
    )
    data["email"] = data["email"].apply(
        lambda x: validate_and_normalize_email(str(x)) if pd.notnull(x) else None
    )
    data["name"] = data["name"].apply(clean_name)
    data["firstname"] = data["firstname"].apply(clean_name)
    data["idade"] = data["idade"].apply(clean_age)
    data["sexo"] = data["sexo"].apply(lambda x: x.strip().upper() if pd.notnull(x) else None)
    data["onde"] = data["onde"].apply(clean_source)
    data["date"] = data["date"].apply(clean_date)

    data = data[data["tel"].notnull()]
    return data

def generate_dashboard(data):
    st.markdown("## Dashboard Interativo")
    
    st.markdown("### Proporção de Dados Válidos vs. Inválidos")
    valid_phones = data["tel"].notnull().sum()
    invalid_phones = len(data) - valid_phones
    valid_emails = data["email"].notnull().sum()
    invalid_emails = len(data) - valid_emails
    
    st.markdown(f"""
    - **Telefones válidos:** {valid_phones}
    - **Telefones inválidos:** {invalid_phones}
    - **E-mails válidos:** {valid_emails}
    - **E-mails inválidos:** {invalid_emails}
    """)

    fig, ax = plt.subplots()
    ax.bar(["Válidos", "Inválidos"], [valid_phones, invalid_phones], color=["#4caf50", "#f44336"])
    ax.set_title("Proporção de Telefones Válidos vs. Inválidos")
    ax.set_ylabel("Quantidade")
    st.pyplot(fig)

    st.markdown("### Distribuição dos DDDs")
    if "tel" in data.columns:
        ddds = data["tel"].dropna().str[3:5]
        ddds_counts = ddds.value_counts()
        
        top_ddds = ddds_counts.head(10)
        fig, ax = plt.subplots()
        top_ddds.sort_values(ascending=False).plot(kind="bar", ax=ax, color="#4caf50")
        ax.set_title("Top 10 DDDs Mais Frequentes")
        ax.set_xlabel("DDD")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

        st.markdown("#### Lista Completa de DDDs")
        st.markdown("```")
        for ddd, count in ddds_counts.items():
            st.markdown(f"DDD {ddd}: {count}")
        st.markdown("```")

    st.markdown("### Origem dos Leads")
    if "onde" in data.columns:
        source_counts = data["onde"].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=source_counts.index, y=source_counts.values, ax=ax, palette="coolwarm")
        ax.set_title("Origem dos Leads")
        ax.set_xlabel("Origem")
        ax.set_ylabel("Frequência")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)

st.title("CSV Cleaner - Flush")

uploaded_file = st.file_uploader("Faça o upload de um arquivo CSV", type=["csv"])

if uploaded_file:
    with st.spinner("Processando o arquivo..."):
        cleaned_data = process_csv(uploaded_file)

    st.success("Arquivo processado com sucesso!")

    csv_buffer = io.StringIO()
    cleaned_data.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Baixar CSV Limpo",
        data=csv_buffer.getvalue(),
        file_name="cleaned_data.csv",
        mime="text/csv",
    )

    generate_dashboard(cleaned_data)
