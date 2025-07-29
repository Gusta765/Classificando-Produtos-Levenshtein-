import pandas as pd
from typing import Tuple

def load_csv_files(internal_file: str, external_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:

    try:
        df_internal = pd.read_csv(internal_file)
        df_external = pd.read_csv(external_file)
        
        print(f"Arquivo interno carregado: {len(df_internal)} produtos")
        print(f"Arquivo externo carregado: {len(df_external)} produtos")
        
        return df_internal, df_external
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        raise
    except Exception as e:
        print(f"Erro ao carregar arquivos: {e}")
        raise

def validate_dataframes(df_internal: pd.DataFrame, df_external: pd.DataFrame) -> bool:

    required_internal_cols = ['CODIGO_INTERNO', 'DESCRICAO']
    required_external_cols = ['CODIGO_EXTERNO', 'DESCRICAO']
    
    if not all(col in df_internal.columns for col in required_internal_cols):
        print(f"Arquivo interno deve conter as colunas: {required_internal_cols}")
        return False
    
    if not all(col in df_external.columns for col in required_external_cols):
        print(f"Arquivo externo deve conter as colunas: {required_external_cols}")
        return False
    
    print("Estrutura dos arquivos validada com sucesso")
    return True