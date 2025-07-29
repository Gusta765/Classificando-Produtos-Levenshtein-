import re
import unicodedata
from typing import List, Tuple
import pandas as pd

class ProductMatcher:
    
    def __init__(self):

        self.synonyms = {
            'quilograma': ['kg', 'kilo'],
            'grama': ['g', 'gr'],
            'mililitro': ['ml'],
            'litro': ['l', 'lt'],
            'pacote': ['pct', 'pack'],
            'caixa': ['cx'],
            'garrafa': ['gar', 'pet'],
            'lata': ['lt'],
            'unidade': ['un', 'und'],
            'integral': ['int'],
            'natural': ['nat']
        }
    
    def normalize_text(self, text: str) -> str:

        if pd.isna(text):
            return ""
        
        text = str(text).lower()
        
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        
        for canonical, variants in self.synonyms.items():
            for variant in variants:
                text = re.sub(r'\b' + re.escape(variant) + r'\b', canonical, text)
        
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def levenshtein_distance(self, s1: str, s2: str) -> int:

        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def similarity_score(self, s1: str, s2: str) -> float:

        norm_s1 = self.normalize_text(s1)
        norm_s2 = self.normalize_text(s2)
        
        distance = self.levenshtein_distance(norm_s1, norm_s2)
        max_len = max(len(norm_s1), len(norm_s2))
        
        if max_len == 0:
            return 1.0
        
        return 1 - (distance / max_len)
    
    def find_best_matches(self, internal_product: str, external_df: pd.DataFrame, top_k: int = 3) -> List[Tuple[str, str, float]]:

        similarities = []
        
        for _, row in external_df.iterrows():
            score = self.similarity_score(internal_product, row['DESCRICAO'])
            similarities.append((
                row['CODIGO_EXTERNO'], 
                row['DESCRICAO'], 
                score
            ))
        
        similarities.sort(key=lambda x: x[2], reverse=True)
        return similarities[:top_k]

def process_products(df_internal: pd.DataFrame, df_external: pd.DataFrame) -> List[dict]:

    matcher = ProductMatcher()
    results = []
    
    total_products = len(df_internal)
    
    for idx, internal_row in df_internal.iterrows():
        print(f"🔍 Processando {idx + 1}/{total_products}: {internal_row['DESCRICAO']}")
        
        best_matches = matcher.find_best_matches(
            internal_row['DESCRICAO'],
            df_external,
            top_k=3
        )
        
        for rank, (codigo_externo, desc_externa, score) in enumerate(best_matches, 1):
            results.append({
                'CODIGO_INTERNO': internal_row['CODIGO_INTERNO'],
                'DESCRICAO_INTERNA': internal_row['DESCRICAO'],
                'RANKING': rank,
                'CODIGO_EXTERNO': codigo_externo,
                'DESCRICAO_EXTERNA': desc_externa,
                'SCORE_SIMILARIDADE': round(score, 4)
            })
    
    return results