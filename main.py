"""
Sistema de Classificação de Produtos com Algoritmo de Levenshtein
=================================================================

Autor: [Gustavo]
Data: 2025

Este sistema compara produtos internos com uma base externa usando 
o algoritmo de distância de Levenshtein para encontrar as melhores 
correspondências baseadas na similaridade de texto.
"""

import sys
from config import internal_file, external_file, output_file
from extract import load_csv_files, validate_dataframes
from transform import process_products
from load import save_results, generate_report, show_best_examples, show_problematic_cases, export_summary_report

def main():
    
    try:
        print("ETAPA 1: CARREGANDO DADOS")
        print("-" * 30)
        df_internal, df_external = load_csv_files(internal_file, external_file)
        
        if not validate_dataframes(df_internal, df_external):
            print("Validação falhou. Encerrando programa.")
            return
        
        print(f"\n🔄 ETAPA 2: PROCESSANDO PRODUTOS")
        print("-" * 30)
        results = process_products(df_internal, df_external)
        
        if not results:
            print("Nenhum resultado gerado. Encerrando programa.")
            return
        
        print(f"\nETAPA 3: SALVANDO RESULTADOS")
        print("-" * 30)
        df_results = save_results(results, output_file)
        
        generate_report(df_results)
        show_best_examples(df_results)
        show_problematic_cases(df_results)
        
        export_summary_report(df_results)
        
        print(f"\nPROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print(f"   - relatorio_resumo.txt (resumo estatístico)")
        
    except FileNotFoundError:
        print(f"Erro: Certifique-se de que os arquivos existem:")
        print(f"   - {internal_file}")
        print(f"   - {external_file}")
        
    except Exception as e:
        print(f"Erro inesperado: {e}")
        print("Verifique se os dados estão no formato correto")

def run_demo():
    
    print("MODO DEMONSTRAÇÃO")
    print("=" * 30)
    
    import pandas as pd
    from transform import ProductMatcher
    
    internal_products = [
        "LEITE INTEGRAL NESTLE 1L CAIXA",
        "ARROZ BRANCO TIOJOAO 5KG",
        "CAFE PILAO 500G VACUO"
    ]
    
    external_products = [
        "LEITE UHT INTEGRAL NESTLE 1000ML TETRA PAK",
        "ARROZ POLIDO TIO JOAO TIPO 1 SACO 5KG", 
        "CAFE TORRADO MOIDO PILAO 500G A VACUO",
        "CHOCOLATE NESCAU 400G LATA"
    ]
    
    matcher = ProductMatcher()
    
    print("Demonstração do algoritmo:\n")
    
    for i, internal in enumerate(internal_products):
        print(f"Produto Interno: {internal}")
        
        best_match = ""
        best_score = 0
        
        for external in external_products:
            score = matcher.similarity_score(internal, external)
            if score > best_score:
                best_score = score
                best_match = external
        
        print(f"Melhor Match: {best_match}")
        print(f"Score: {best_score:.4f}")
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        main()