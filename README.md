# LH Nautical Dashboard

Dashboard executivo para apresentação dos resultados do desafio Lighthouse.

## Objetivo

Apresentar de forma visual os principais resultados das questões 1 a 7, com foco em:

- faturamento por dia da semana
- melhor dia do ciclo comercial
- previsão de demanda para Q1/2026
- indicadores executivos do negócio

## Estrutura do projeto

- `app.py` — aplicação Streamlit
- `requirements.txt` — dependências do projeto
- `LH_Nautical_Outputs/` — arquivos CSV/JSON gerados pela análise
- `LH_Dashboard_Final_Questões.ipynb` — notebook com a análise completa

## Como executar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Crie um repositório no GitHub.
2. Envie este projeto para a branch desejada.
3. No Streamlit Cloud, conecte seu repositório.
4. Selecione a branch e o arquivo `app.py` como ponto de entrada.

## Observação

A aplicação lê os arquivos exportados em `LH_Nautical_Outputs`, então o notebook deve ser executado antes do deploy para garantir que os dados estejam atualizados.
