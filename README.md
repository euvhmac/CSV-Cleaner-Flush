# CSV Cleaner - Flush
🚀 Uma ferramenta interativa e altamente funcional para limpeza, validação e padronização de dados em arquivos CSV. Desenvolvido com **Python** e **Streamlit**, este projeto foi cuidadosamente planejado e executado para destacar habilidades em análise de dados, organização e metodologias ágeis.

![CSV Cleaner - Dashboard](assets/dashboard_example.png)

---

## 🌟 **Principais Funcionalidades**
- **Validação e formatação de números de telefone**:
  - Detecta e corrige números de telefone brasileiros no formato `<DDD><9><número de 8 dígitos>`.
  - Exclui automaticamente leads sem números válidos.

- **Normalização e validação de e-mails**:
  - Corrige pequenos erros de digitação, como `.con` ou `.co`.
  - Valida o domínio e corrige para domínios conhecidos.

- **Dashboards interativos**:
  - Proporção de dados válidos vs. inválidos.
  - Distribuição de DDDs por frequência.
  - Origem dos leads (dados categóricos).

- **Organização de dados**:
  - Padroniza nomes, datas, idades e outros campos para consistência.

---

## 📊 **Dashboards**
### **1. Proporção de Dados Válidos vs. Inválidos**
Uma visão clara da qualidade dos dados, destacando números e e-mails válidos.

### **2. Distribuição de DDDs**
Gráfico de barras mostrando a frequência dos DDDs mais usados. Insights importantes para campanhas regionais.

### **3. Origem dos Leads**
Análise categórica que exibe as principais fontes de aquisição de dados (por exemplo: redes sociais, campanhas específicas).

---

## 🛠️ **Tecnologias Utilizadas**
- **Python 3.9+**
- **Streamlit**: Interface interativa.
- **Pandas**: Manipulação e limpeza de dados.
- **Matplotlib/Seaborn**: Visualização de dados.
- **Email-validator**: Validação de e-mails.
- **Phonenumbers**: Validação e formatação de números de telefone.

---

## 📂 **Organização e Planejamento**
Este projeto foi estruturado e executado com metodologias ágeis, utilizando o **Jira** para organização e acompanhamento das tarefas. O desenvolvimento foi dividido em **épicos, sprints e tarefas** específicas para manter o progresso consistente e alinhado aos objetivos.

### **Exemplo de Organização no Jira**:
- **Épico**: Desenvolvimento do CSV Cleaner.
  - **Sprint 1**: Validação e limpeza de números de telefone.
    - Tarefa: Implementar lógica de validação de DDDs.
    - Tarefa: Excluir linhas sem número válido.
  - **Sprint 2**: Normalização de e-mails.
    - Tarefa: Corrigir pequenos erros de digitação em e-mails.
    - Tarefa: Validar domínios conhecidos.
  - **Sprint 3**: Dashboards Interativos.
    - Tarefa: Criar gráficos de distribuição de DDDs.
    - Tarefa: Exibir proporção de dados válidos vs. inválidos.

![CSV Cleaner - Dashboard](assets/dashboard_jira1.png)

![CSV Cleaner - Dashboard](assets/dashboard_jira2.png)

Essa abordagem destaca habilidades como **planejamento**, **gestão de projetos** e **organização de tarefas**, que são essenciais em ambientes corporativos.

---

## 🚀 **Como Usar**
### 1. Clone o Repositório:
```bash
git clone https://github.com/YOUR-USERNAME/csv-cleaner-flush.git
cd csv-cleaner-flush
