# 📂 Classificador de Produtos com Levenshtein

## 📖 Descrição

Este projeto é um pipeline de **ETL (Extract, Transform, Load)** desenvolvido em Python para resolver um problema comum em e-commerces e sistemas de gestão: a falta de padronização em cadastros de produtos.

Utilizando uma abordagem algorítmica baseada na **Distância de Levenshtein**, o sistema compara uma lista de produtos "interna" (do seu sistema) com uma lista "externa" (de um fornecedor, por exemplo) e encontra as correspondências mais prováveis, mesmo que as descrições não sejam idênticas.

O objetivo principal é limpar, padronizar e enriquecer bases de dados de produtos, reduzindo a duplicidade e facilitando análises de negócio.

---

## ✨ Funcionalidades Principais

* **Pipeline ETL Completo:** O projeto é dividido em etapas claras de Extração, Transformação e Carga.
* **Normalização Avançada de Texto:** Realiza uma limpeza profunda nas descrições dos produtos antes da comparação, incluindo:
    * Remoção de acentos e caracteres especiais.
    * Conversão para minúsculas.
    * Expansão de sinônimos e abreviações (ex: `kg` -> `quilograma`, `pct` -> `pacote`).
* **Algoritmo de Levenshtein:** A distância é calculada para medir a "diferença" entre duas strings, servindo como base para o score de similaridade.
* **Ranking de Matches:** Para cada produto interno, o sistema gera um ranking com os 3 melhores candidatos da base externa, junto com um score de similaridade (0 a 1).
* **Geração de Relatórios:** Ao final do processo, são gerados:
    * Um arquivo `.csv` com o resultado completo da classificação.
    * Um relatório de resumo `.txt` com estatísticas sobre a qualidade dos matches.
    * Visualização dos melhores e piores casos diretamente no terminal.

---

## 🚀 Como Usar

### Pré-requisitos

* Python 3.8+
* Pandas (`pip install pandas`)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Instale as dependências:**
    (Recomenda-se criar um ambiente virtual)
    ```bash
    pip install -r requirements.txt
    ```
    *Obs: Certifique-se de criar um arquivo `requirements.txt` contendo `pandas`.*

### Configuração

1.  **Prepare seus arquivos de dados:**
    * Crie um arquivo `produtos_internos.csv` com as colunas `CODIGO_INTERNO` e `DESCRICAO`.
    * Crie um arquivo `produtos_externos.csv` com as colunas `CODIGO_EXTERNO` e `DESCRICAO`.
    * Coloque ambos na pasta raiz do projeto ou ajuste os caminhos no arquivo `config.py`.

2.  **Ajuste a configuração (opcional):**
    * Você pode alterar os nomes dos arquivos de entrada e saída no `config.py`.

### Execução

1.  **Para rodar o pipeline completo:**
    ```bash
    python main.py
    ```
    Os arquivos `resultado_classificacao.csv` e `relatorio_resumo.txt` serão gerados na pasta raiz.

2.  **Para rodar o modo de demonstração:**
    Este modo não requer arquivos `.csv` e roda com dados de exemplo diretamente no código.
    ```bash
    python main.py --demo
    ```

---

## 🛠️ Estrutura do Projeto

```
.
├── main.py             # Orquestrador do pipeline
├── extract.py          # Funções para carregar e validar os dados
├── transform.py        # Classe ProductMatcher e lógica de normalização/comparação
├── load.py             # Funções para salvar resultados e gerar relatórios
├── config.py           # Configuração dos caminhos dos arquivos
├── produtos_internos.csv  # SEU ARQUIVO de dados internos
└── produtos_externos.csv  # SEU ARQUIVO de dados externos
```

---

## 💡 Lógica Principal

O núcleo do sistema está na classe `ProductMatcher` (`transform.py`). O método `similarity_score` executa os seguintes passos:

1.  Recebe duas strings (descrições de produtos).
2.  Aplica a função `normalize_text` em ambas para limpar e padronizar o texto.
3.  Calcula a `levenshtein_distance` entre as duas strings normalizadas.
4.  Converte a distância em um score de similaridade normalizado entre 0 e 1, onde 1 significa que as strings são idênticas.

```python
def similarity_score(self, s1: str, s2: str) -> float:
    # Normaliza ambas as strings antes de comparar
    norm_s1 = self.normalize_text(s1)
    norm_s2 = self.normalize_text(s2)
    
    # Calcula a distância com o algoritmo de Levenshtein
    distance = self.levenshtein_distance(norm_s1, norm_s2)
    max_len = max(len(norm_s1), len(norm_s2))
    
    # Retorna o score de similaridade (1.0 = match perfeito)
    if max_len == 0:
        return 1.0
    return 1 - (distance / max_len)
```
### 📫 Contato

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gustavo-barbosa-868976236/) [![Email](https://img.shields.io/badge/Email-gustavobarbosa7744@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:gustavobarbosa7744@gmail.com)
