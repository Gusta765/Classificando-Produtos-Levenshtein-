import pandas as pd
from typing import List

def save_results(results: List[dict], output_file: str = 'resultado_classificacao.csv') -> pd.DataFrame:

    try:
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Resultados salvos em: {output_file}")
        return df_results
        
    except Exception as e:
        print(f"Erro ao salvar resultados: {e}")
        raise

def generate_report(df_results: pd.DataFrame):

    if df_results.empty:
        print("Nenhum resultado para analisar")
        return
    
    print("\n" + "="*60)
    print("RELATÓRIO DE ANÁLISE")
    print("="*60)
    
    total_comparisons = len(df_results)
    unique_products = df_results['CODIGO_INTERNO'].nunique()
    
    print(f"Total de comparações: {total_comparisons}")
    print(f"Produtos processados: {unique_products}")
    
    best_matches = df_results[df_results['RANKING'] == 1]
    avg_score = best_matches['SCORE_SIMILARIDADE'].mean()
    
    print(f"Score médio dos melhores matches: {avg_score:.4f}")
    
    high_quality = len(best_matches[best_matches['SCORE_SIMILARIDADE'] >= 0.8])
    medium_quality = len(best_matches[best_matches['SCORE_SIMILARIDADE'] >= 0.6])
    low_quality = len(best_matches[best_matches['SCORE_SIMILARIDADE'] < 0.6])
    
    print(f"\nDistribuição de Qualidade (Melhores Matches):")
    print(f"Alta similaridade (≥80%): {high_quality} produtos ({high_quality/len(best_matches)*100:.1f}%)")
    print(f"Média similaridade (≥60%): {medium_quality} produtos ({medium_quality/len(best_matches)*100:.1f}%)")
    print(f"Baixa similaridade (<60%): {low_quality} produtos ({low_quality/len(best_matches)*100:.1f}%)")

def show_best_examples(df_results: pd.DataFrame, top_n: int = 5):

    print(f"\nTOP {top_n} MELHORES CORRESPONDÊNCIAS:")
    print("="*80)
    
    best_matches = df_results[df_results['RANKING'] == 1]
    top_matches = best_matches.nlargest(top_n, 'SCORE_SIMILARIDADE')
    
    for idx, row in top_matches.iterrows():
        print(f"\nScore: {row['SCORE_SIMILARIDADE']:.4f}")
        print(f"Interno:  {row['DESCRICAO_INTERNA']}")
        print(f"Externo:  {row['DESCRICAO_EXTERNA']}")
        print("-" * 80)

def show_problematic_cases(df_results: pd.DataFrame, bottom_n: int = 3):

    print(f"\n {bottom_n} CASOS MAIS PROBLEMÁTICOS:")
    print("="*80)
    
    best_matches = df_results[df_results['RANKING'] == 1]
    problematic = best_matches.nsmallest(bottom_n, 'SCORE_SIMILARIDADE')
    
    for idx, row in problematic.iterrows():
        print(f"\nScore: {row['SCORE_SIMILARIDADE']:.4f}")
        print(f"Interno:  {row['DESCRICAO_INTERNA']}")
        print(f"Melhor Match: {row['DESCRICAO_EXTERNA']}")
        print("-" * 80)

def export_summary_report(df_results: pd.DataFrame, summary_file: str = 'relatorio_resumo.txt'):

    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE CLASSIFICAÇÃO DE PRODUTOS\n")
            f.write("="*50 + "\n\n")
            
            best_matches = df_results[df_results['RANKING'] == 1]
            avg_score = best_matches['SCORE_SIMILARIDADE'].mean()
            
            f.write(f"Total de produtos processados: {len(best_matches)}\n")
            f.write(f"Score médio de similaridade: {avg_score:.4f}\n\n")
            
            high_quality = len(best_matches[best_matches['SCORE_SIMILARIDADE'] >= 0.8])
            medium_quality = len(best_matches[best_matches['SCORE_SIMILARIDADE'] >= 0.6])
            
            f.write("DISTRIBUIÇÃO DE QUALIDADE:\n")
            f.write(f"Alta similaridade (≥80%): {high_quality} produtos\n")
            f.write(f"Média similaridade (≥60%): {medium_quality} produtos\n")
            f.write(f"Baixa similaridade (<60%): {len(best_matches) - medium_quality} produtos\n")
        
        print(f"📄 Relatório resumo salvo em: {summary_file}")
        
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")