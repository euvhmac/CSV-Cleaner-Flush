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
    11, 12, 13, 14, 15, 16, 17, 18, 19,  # São Paulo
    21, 22, 24,                        # Rio de Janeiro
    27, 28,                            # Espírito Santo
    31, 32, 33, 34, 35, 37, 38,        # Minas Gerais
    41, 42, 43, 44, 45, 46,            # Paraná
    47, 48, 49,                        # Santa Catarina
    51, 53, 54, 55,                    # Rio Grande do Sul
    61,                                # Distrito Federal
    62, 64,                            # Goiás
    63,                                # Tocantins
    65, 66,                            # Mato Grosso
    67,                                # Mato Grosso do Sul
    68,                                # Acre
    69,                                # Rondônia
    71, 73, 74, 75, 77,                # Bahia
    79,                                # Sergipe
    81, 87,                            # Pernambuco
    82,                                # Alagoas
    83,                                # Paraíba
    84,                                # Rio Grande do Norte
    85, 88,                            # Ceará
    86, 89,                            # Piauí
    91, 93, 94,                        # Pará
    92, 97,                            # Amazonas
    95,                                # Roraima
    96,                                # Amapá
    98, 99                             # Maranhão
}

# Função para processar o CSV
def process_csv(file):
    data = pd.read_csv(file)

    # Padronizar os dados
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

    # Excluir linhas sem número de telefone
    data = data[data["tel"].notnull()]
    return data

# Função para gerar gráficos
def generate_dashboard(data):
    st.markdown("## Dashboard Interativo")
    
    # Proporção de Dados Válidos vs. Inválidos
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

    # Gráfico: Proporção de Telefones Válidos vs. Inválidos
    fig, ax = plt.subplots()
    ax.bar(["Válidos", "Inválidos"], [valid_phones, invalid_phones], color=["#4caf50", "#f44336"])
    ax.set_title("Proporção de Telefones Válidos vs. Inválidos")
    ax.set_ylabel("Quantidade")
    st.pyplot(fig)

    # Distribuição dos DDDs
    st.markdown("### Distribuição dos DDDs")
    if "tel" in data.columns:
        # Extrair os DDDs
        ddds = data["tel"].dropna().str[3:5]  # Pegar os dois números após "+55"
        ddds_counts = ddds.value_counts()
        
        # Exibir os 10 DDDs mais frequentes no gráfico
        top_ddds = ddds_counts.head(10)
        fig, ax = plt.subplots()
        top_ddds.sort_values(ascending=False).plot(kind="bar", ax=ax, color="#4caf50")
        ax.set_title("Top 10 DDDs Mais Frequentes")
        ax.set_xlabel("DDD")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

        # Mostrar a lista completa de DDDs em formato Markdown
        st.markdown("#### Lista Completa de DDDs")
        st.markdown("```")
        for ddd, count in ddds_counts.items():
            st.markdown(f"DDD {ddd}: {count}")
        st.markdown("```")

    # Origem dos Leads
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

# Configuração do Streamlit
st.title("CSV Cleaner - Flush")

uploaded_file = st.file_uploader("Faça o upload de um arquivo CSV", type=["csv"])

if uploaded_file:
    with st.spinner("Processando o arquivo..."):
        cleaned_data = process_csv(uploaded_file)

    st.success("Arquivo processado com sucesso!")

    # Botão para download da planilha limpa
    csv_buffer = io.StringIO()
    cleaned_data.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Baixar CSV Limpo",
        data=csv_buffer.getvalue(),
        file_name="cleaned_data.csv",
        mime="text/csv",
    )

    # Gerar Dashboard
    generate_dashboard(cleaned_data)
