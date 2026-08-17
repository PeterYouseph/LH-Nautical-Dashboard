from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "LH_Nautical_Outputs"

st.set_page_config(
    page_title="LH Nautical Dashboard",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 LH Nautical - Dashboard Executivo")
st.caption("Análise de vendas, desempenho por dia da semana e previsão de demanda")


@st.cache_data
def load_report():
    report_path = OUTPUTS_DIR / "RELATORIO_FINAL.json"
    if report_path.exists():
        with report_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "status": "Arquivo de relatório não encontrado",
        "questoes": {},
    }


@st.cache_data
def load_sales_by_weekday():
    path = OUTPUTS_DIR / "Q5_Vendas_Dia_Semana.csv"
    if path.exists():
        df = pd.read_csv(path)
        df["Faturamento_R$"] = pd.to_numeric(df["Faturamento_R$"], errors="coerce").fillna(0)
        return df
    return pd.DataFrame(
        {
            "Dia_Semana": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
            "Faturamento_R$": [197_909_345.77, 203_633_659.11, 205_294_168.39, 197_798_236.35, 203_011_799.60, 200_204_288.40, 198_635_704.18],
        }
    )


@st.cache_data
def load_forecast():
    path = OUTPUTS_DIR / "Q6_Forecast_Bussola.csv"
    if path.exists():
        df = pd.read_csv(path)
        qty_col = "Quantidade_Prevista" if "Quantidade_Prevista" in df.columns else "Quantidade"
        df = df.rename(columns={qty_col: "Quantidade_Prevista"})
        df["Quantidade_Prevista"] = pd.to_numeric(df["Quantidade_Prevista"], errors="coerce").fillna(0)
        return df
    return pd.DataFrame(
        {
            "Mes": ["2026-01", "2026-02", "2026-03"],
            "Quantidade_Prevista": [25, 25, 21],
        }
    )


report = load_report()
sales_by_weekday = load_sales_by_weekday()
forecast = load_forecast()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Ticket médio", "R$ 28.704,99")

with kpi2:
    melhor_dia = sales_by_weekday.loc[sales_by_weekday["Faturamento_R$"].idxmax(), "Dia_Semana"]
    melhor_valor = sales_by_weekday["Faturamento_R$"].max()
    st.metric("Melhor dia", f"{melhor_dia}", f"R$ {melhor_valor:,.2f}")

with kpi3:
    total_forecast = int(forecast["Quantidade_Prevista"].sum())
    st.metric("Forecast Q1/2026", f"{total_forecast} unidades")

with kpi4:
    total_faturamento = float(sales_by_weekday["Faturamento_R$"].sum())
    st.metric("Faturamento total", f"R$ {total_faturamento:,.2f}")

st.subheader("📈 Faturamento por dia da semana")
fig_bar = px.bar(
    sales_by_weekday,
    x="Dia_Semana",
    y="Faturamento_R$",
    color="Faturamento_R$",
    color_continuous_scale="Viridis",
    title="Distribuição do faturamento por dia da semana",
)
fig_bar.update_layout(height=500)
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("🧭 Previsão de demanda do produto Bústula de Bordo 702")
fig_line = px.line(
    forecast,
    x="Mes",
    y="Quantidade_Prevista",
    markers=True,
    title="Previsão por mês (Q1/2026)",
)
fig_line.update_layout(height=400)
st.plotly_chart(fig_line, use_container_width=True)

with st.sidebar:
    st.header("Resumo Executivo")
    st.write("Status:", report.get("status", "Em análise"))

    if report.get("questoes"):
        for key, value in report["questoes"].items():
            st.markdown(f"- **{key}**: {value.get('titulo', key)}")
    else:
        st.markdown("- Q1: Ticket Médio")
        st.markdown("- Q2: Schema do Banco de Dados")
        st.markdown("- Q3: PostgreSQL Loader")
        st.markdown("- Q4: Top 10 Clientes")
        st.markdown("- Q5: Vendas por Dia da Semana")
        st.markdown("- Q6: Forecast Q1/2026")
        st.markdown("- Q7: Recomendação de Produtos")

    st.markdown("---")
    st.markdown("Dashboard montado a partir dos arquivos exportados em [LH_Nautical_Outputs](LH_Nautical_Outputs).")

st.markdown("### ✅ Observações")
st.write(
    "A interface usa dados já exportados do notebook para apresentar o painel em formato executivo, "
    "permitindo uma leitura rápida para cliente, área comercial ou apresentação final."
)
