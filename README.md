# LH Nautical Dashboard

Dashboard executivo de análise comercial para a operação de varejo e distribuição marítima da LH Nautical.

## Visão geral

Este projeto foi desenvolvido para transformar dados de pedidos, produtos, clientes e movimentação comercial em uma visão executiva do negócio. O objetivo é apoiar a tomada de decisão com indicadores de desempenho, identificação de clientes de maior valor e previsão de demanda para os principais itens do catálogo.

A análise cobre os principais pontos de negócio da operação, incluindo:

- ticket médio e comportamento financeiro
- estrutura e qualidade do modelo de dados
- métricas de faturamento por dia da semana
- identificação de clientes estratégicos
- projeção de demanda para o produto Bústula de Bordo 702
- recomendações de produtos com comportamento semelhante

## Case de negócio

A LH Nautical opera em um ambiente de varejo de produtos náuticos, com alta diversidade de itens e múltiplas tabelas de dados transacionais. Nesse contexto, o desafio foi consolidar informações espalhadas em diferentes fontes para responder perguntas críticas de gestão, como:

- qual é o ticket médio da operação?
- como está distribuído o faturamento ao longo da semana?
- quem são os clientes mais relevantes em valor e diversidade de compra?
- qual será a demanda esperada para um item estratégico?
- quais produtos têm maior afinidade entre si para apoiar ações de recomendação e cross-sell?

## Estrutura do projeto

- `app.py` — aplicação Streamlit com dashboard executivo
- `requirements.txt` — dependências da aplicação
- `LH_Nautical_Outputs/` — arquivos exportados com resultados e relatórios
- `LH_Dashboard_Final_Questões.ipynb` — notebook com a análise completa e a construção dos indicadores

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
3. Conecte o repositório no Streamlit Cloud.
4. Selecione a branch e o arquivo `app.py` como ponto de entrada.

## Observação

A aplicação lê os arquivos exportados em `LH_Nautical_Outputs`, então o notebook deve ser executado antes do deploy para garantir que os dados estejam atualizados.
