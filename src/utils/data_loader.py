import pandas as pd

def load_data(file_path):
    """
    Carrega um arquivo CSV em um DataFrame do pandas.
    
    :param file_path: Caminho para o arquivo CSV.
    :return: DataFrame com os dados carregados ou None se houver erro.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Dados carregados com sucesso! {data.shape[0]} linhas, {data.shape[1]} colunas.")
        return data
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado no caminho especificado: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Erro: O arquivo {file_path} está vazio.")
        return None
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None
