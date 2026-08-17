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

st.markdown(
    """
    <style>
        .stApp {
            background: var(--background-color);
            color: var(--text-color);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        [data-testid="stSidebar"] {
            background: var(--secondary-background-color);
        }
        h1 {
            color: var(--text-color);
            font-weight: 800;
        }
        .subtitle {
            color: var(--text-color);
            opacity: 0.85;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.5rem;
            font-weight: 700;
        }
        div[data-testid="stMetricLabel"] {
            color: var(--text-color);
            opacity: 0.8;
            font-weight: 600;
        }
        .card {
            background: var(--secondary-background-color);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.08);
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 LH Nautical - Dashboard Executivo")
st.markdown(
    '<div class="subtitle">Análise de vendas, desempenho por dia da semana e previsão de demanda</div>',
    unsafe_allow_html=True,
)


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

q1 = report.get("questoes", {}).get("Q1", {})
q2 = report.get("questoes", {}).get("Q2", {})
q3 = report.get("questoes", {}).get("Q3", {})
q4 = report.get("questoes", {}).get("Q4", {})
q5 = report.get("questoes", {}).get("Q5", {})
q6 = report.get("questoes", {}).get("Q6", {})
q7 = report.get("questoes", {}).get("Q7", {})

best_day = q5.get("melhor_dia") or sales_by_weekday.loc[sales_by_weekday["Faturamento_R$"].idxmax(), "Dia_Semana"]
best_value = float(q5.get("faturamento_melhor_dia") or sales_by_weekday["Faturamento_R$"].max())
total_faturamento = float(q5.get("total_faturamento") or sales_by_weekday["Faturamento_R$"].sum())
forecast_total = int(q6.get("forecast_q1_2026") or forecast["Quantidade_Prevista"].sum())
total_tabelas = q2.get("total_tabelas") or len(pd.read_csv(OUTPUTS_DIR / "Q2_Schema.csv"))
clientes_elite = q4.get("clientes_elite") or 10

def money(value):
    return f"R$ {float(value):,.2f}"

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.metric("Ticket médio", money(q1.get("resultado", "28255.58").replace("R$ ", "").replace(".", "").replace(",", ".") if isinstance(q1.get("resultado"), str) else q1.get("resultado", 28255.58)))

with kpi2:
    st.metric("Melhor dia", best_day, money(best_value))

with kpi3:
    st.metric("Faturamento total", money(total_faturamento))

with kpi4:
    st.metric("Forecast Q1/2026", f"{forecast_total} un.")

with kpi5:
    st.metric("Tabelas", total_tabelas)

with kpi6:
    st.metric("Clientes elite", clientes_elite)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📈 Performance comercial por dia da semana")
fig_bar = px.bar(
    sales_by_weekday,
    x="Dia_Semana",
    y="Faturamento_R$",
    color="Faturamento_R$",
    color_continuous_scale="Viridis",
    title="Faturamento por dia da semana",
)
fig_bar.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=500,
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
fig_bar.update_traces(marker_line_width=0)
st.plotly_chart(fig_bar, width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🧭 Previsão de demanda")
fig_line = px.line(
    forecast,
    x="Mes",
    y="Quantidade_Prevista",
    markers=True,
    title="Demanda projetada para o primeiro trimestre de 2026",
)
fig_line.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=420,
    margin=dict(l=10, r=10, t=40, b=10),
)
fig_line.update_traces(line=dict(width=3), marker=dict(size=8))
st.plotly_chart(fig_line, width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Resumo Executivo")
    st.write("Status:", report.get("status", "Em análise"))

    st.markdown("### Principais entregas")
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
    st.caption("Dashboard gerado a partir dos arquivos exportados em LH_Nautical_Outputs.")

st.markdown("### ✅ Observações")
st.write(
    "Em caso de divergências nos dados, recomenda-se revisar os arquivos exportados em LH_Nautical_Outputs e validar as métricas diretamente no banco de dados ou nas planilhas originais."
)
