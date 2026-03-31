import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    layout="wide",
    page_title="GYM Shop | Command Center",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

    * { box-sizing: border-box; }

    .stApp {
        background-color: #080A0F;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(79,172,254,0.08) 0%, transparent 60%),
            radial-gradient(ellipse 40% 30% at 80% 80%, rgba(248,81,73,0.05) 0%, transparent 50%);
        font-family: 'DM Sans', sans-serif;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1117 0%, #080A0F 100%);
        border-right: 1px solid rgba(79,172,254,0.15);
    }
    [data-testid="stSidebar"] * { color: #C9D1D9 !important; }

    /* ── HEADER BRAND ── */
    .brand-header {
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin-bottom: 4px;
    }
    .brand-name {
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
    }
    .brand-tag {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: #4facfe;
        background: rgba(79,172,254,0.1);
        border: 1px solid rgba(79,172,254,0.3);
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 1.5px;
    }
    .brand-sub {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        color: #4B5563;
        letter-spacing: 0.5px;
    }

    /* ── HEALTH SCORE BANNER ── */
    .health-banner {
        background: linear-gradient(135deg, #0D1117 0%, #111827 100%);
        border: 1px solid rgba(79,172,254,0.2);
        border-radius: 16px;
        padding: 20px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .health-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4facfe, transparent);
    }
    .health-score-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: #4B5563;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .health-score-value {
        font-family: 'Syne', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -2px;
    }
    .health-score-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        color: #6B7280;
        margin-top: 4px;
    }

    /* ── KPI CARDS ── */
    .kpi-card {
        background: #0D1117;
        border: 1px solid #1C2333;
        border-radius: 14px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s, transform 0.2s;
        height: 100%;
    }
    .kpi-card:hover { border-color: rgba(79,172,254,0.4); transform: translateY(-2px); }
    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 0 0 14px 14px;
    }
    .kpi-card.blue::after  { background: linear-gradient(90deg, #4facfe, #00f2fe); }
    .kpi-card.green::after { background: linear-gradient(90deg, #2EA043, #56d364); }
    .kpi-card.red::after   { background: linear-gradient(90deg, #F85149, #ff6b6b); }
    .kpi-card.gold::after  { background: linear-gradient(90deg, #D29922, #f0c040); }

    .kpi-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        color: #4B5563;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #F0F6FC;
        line-height: 1;
        margin-bottom: 8px;
    }
    .kpi-delta {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .kpi-icon {
        position: absolute;
        top: 18px; right: 18px;
        font-size: 1.4rem;
        opacity: 0.25;
    }

    /* ── SECTION HEADERS ── */
    .section-header {
        font-family: 'Syne', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #4B5563;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 24px 0 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #1C2333, transparent);
    }

    /* ── CHART CONTAINERS ── */
    .chart-box {
        background: #0D1117;
        border: 1px solid #1C2333;
        border-radius: 14px;
        padding: 20px;
        height: 100%;
    }
    .chart-box-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #8B949E;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    .chart-box-sub {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        color: #30363D;
        margin-bottom: 14px;
        letter-spacing: 1px;
    }

    /* ── TICKET CHIPS ── */
    .ticket-chip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid;
    }
    .ticket-chip.danger  { background: rgba(248,81,73,0.07);  border-color: rgba(248,81,73,0.25); }
    .ticket-chip.warning { background: rgba(210,153,34,0.07); border-color: rgba(210,153,34,0.25); }
    .ticket-chip.info    { background: rgba(88,166,255,0.07); border-color: rgba(88,166,255,0.25); }
    .chip-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 1px;
    }
    .chip-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        line-height: 1;
    }
    .chip-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        opacity: 0.6;
        margin-top: 2px;
    }

    /* ── CALENDARIO PILLS ── */
    .cal-pill {
        display: inline-block;
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        padding: 2px 8px;
        border-radius: 20px;
        margin: 2px;
        white-space: nowrap;
    }
    .cal-pill.conf    { background: rgba(46,160,67,0.15);  color: #56d364; border: 1px solid rgba(46,160,67,0.3); }
    .cal-pill.pconf   { background: rgba(210,153,34,0.15); color: #f0c040; border: 1px solid rgba(210,153,34,0.3); }
    .cal-pill.pend    { background: rgba(88,166,255,0.15); color: #79c0ff; border: 1px solid rgba(88,166,255,0.3); }
    .cal-pill.reprog  { background: rgba(248,81,73,0.15);  color: #ff7b72; border: 1px solid rgba(248,81,73,0.3); }
    .cal-pill.ejec    { background: rgba(139,148,158,0.15);color: #8b949e; border: 1px solid rgba(139,148,158,0.3); }

    /* ── ALERTS ── */
    .alert-strip {
        border-radius: 8px;
        padding: 8px 16px;
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: 0.5px;
    }
    .alert-strip.warn { background: rgba(210,153,34,0.08); border: 1px solid rgba(210,153,34,0.25); color: #D29922; }
    .alert-strip.info { background: rgba(88,166,255,0.08); border: 1px solid rgba(88,166,255,0.25); color: #58A6FF; }

    /* ── CORTE BADGE ── */
    .corte-badge {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: #4facfe;
        background: rgba(79,172,254,0.08);
        border: 1px solid rgba(79,172,254,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        letter-spacing: 1px;
    }

    /* ── HIDE STREAMLIT CHROME ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# PLOTLY THEME HELPERS
# ==========================================
PLOTLY_BASE = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#8B949E"),
    margin=dict(t=10, b=10, l=10, r=10),
)

def style_fig(fig, **kwargs):
    fig.update_layout(**PLOTLY_BASE, **kwargs)
    fig.update_xaxes(gridcolor="#1C2333", zeroline=False, tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="#1C2333", zeroline=False, tickfont=dict(size=11))
    return fig

# ==========================================
# CARGA DE DATOS
# ==========================================
_THIS_FILE = Path(__file__).resolve()
_CANDIDATES = [
    Path(os.getcwd()),
    _THIS_FILE.parent,
    Path(os.getcwd()) / "data",
    _THIS_FILE.parent / "data",
]
DATA_DIR = next(
    (p for p in _CANDIDATES if (p / "operaciones.csv").exists()),
    Path(os.getcwd())
)

@st.cache_data(ttl=300)
def load_data():
    df_ops = pd.read_csv(DATA_DIR / "operaciones.csv")
    df_cal = pd.read_csv(DATA_DIR / "calendario.csv")
    df_cal.columns = df_cal.columns.str.strip()

    _meses = {
        "enero":"01","febrero":"02","marzo":"03","abril":"04","mayo":"05","junio":"06",
        "julio":"07","agosto":"08","septiembre":"09","octubre":"10","noviembre":"11","diciembre":"12"
    }
    def _parse_fecha(s):
        s = str(s).lower().strip()
        for m, n in _meses.items():
            s = s.replace(f" de {m} de ", f"/{n}/")
        return pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")

    df_cal["Fecha"] = df_cal["Fecha"].apply(_parse_fecha)
    df_tickets = pd.read_csv(DATA_DIR / "tickets.csv")

    df_ventas = pd.read_csv(DATA_DIR / "ventas.csv")
    df_ventas.columns = df_ventas.columns.str.strip()
    df_ventas["Fecha"] = pd.to_datetime(df_ventas["Fecha"])
    df_ventas["Venta_num"] = (
        df_ventas["Venta día"]
        .str.replace("COP", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
        .astype(float)
    )

    df_ops["% Cumplimiento"] = df_ops.apply(
        lambda r: (r["Visitas registradas"] / r["Agenda semana pasada"] * 100)
        if r["Agenda semana pasada"] > 0 else None,
        axis=1
    )
    return df_ops, df_cal, df_tickets, df_ventas

df_master, df_cal_master, df_tickets, df_ventas = load_data()

# Fecha de corte — compatible Linux/Windows
fecha_corte = df_cal_master["Fecha"].max()
try:
    fecha_corte_str = f"{fecha_corte.day} de {fecha_corte.strftime('%B')} {fecha_corte.year}"
except Exception:
    fecha_corte_str = str(fecha_corte)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
        <div class="brand-header">
            <span class="brand-name">GYM Shop</span>
            <span class="brand-tag">OPS</span>
        </div>
        <div class="brand-sub">COMMAND CENTER · v2.0</div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**FILTROS**")

    lista_tecnicos = ["Ver Todos (Visión Global)"] + sorted(df_master["Técnico"].unique().tolist())
    tec_seleccionado = st.selectbox("Técnico:", lista_tecnicos, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⟳  Recargar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-family:DM Mono,monospace; font-size:0.68rem; color:#4B5563; letter-spacing:1px; margin-bottom:10px;'>LEYENDA AGENDA</div>
        <div style='font-family:DM Mono,monospace; font-size:0.7rem; line-height:2;'>
            <span style='color:#56d364;'>●</span> Confirmado<br>
            <span style='color:#f0c040;'>●</span> Por confirmar<br>
            <span style='color:#79c0ff;'>●</span> Pendiente<br>
            <span style='color:#ff7b72;'>●</span> Reprogramado<br>
            <span style='color:#8b949e;'>●</span> Ejecutado
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Desarrollado por Techforce")

# ==========================================
# APLICAR FILTRO
# ==========================================
if tec_seleccionado == "Ver Todos (Visión Global)":
    df = df_master.copy()
    df_cal = df_cal_master.copy()
    vista_label = "VISIÓN GLOBAL"
    df_v_ops = df_ventas.copy()
else:
    df = df_master[df_master["Técnico"] == tec_seleccionado].copy()
    df_cal = df_cal_master[df_cal_master["Técnico"] == tec_seleccionado].copy()
    vista_label = tec_seleccionado.upper()
    if "Técnico" in df_ventas.columns:
        df_v_ops = df_ventas[df_ventas["Técnico"] == tec_seleccionado].copy()
    else:
        df_v_ops = df_ventas.copy()

# ==========================================
# MÉTRICAS
# ==========================================
total_visitas = int(df["Visitas registradas"].sum())
total_agenda  = int(df["Agenda semana pasada"].sum())
total_gastos  = float(df["Gastos"].sum())
cumplimiento  = (total_visitas / total_agenda * 100) if total_agenda > 0 else 0

df_v_pos   = df_v_ops[df_v_ops["Venta_num"] > 0].copy()
total_venta = df_v_pos["Venta_num"].sum()
ticket_prom = df_v_pos["Venta_num"].mean() if len(df_v_pos) > 0 else 0

total_tickets = int(df_tickets["Cantidad"].sum())
vencidos_sla  = int(df_tickets[df_tickets["Estado"] == "VENCIDOS (SLA)"]["Cantidad"].sum()) \
    if "VENCIDOS (SLA)" in df_tickets["Estado"].values else 0

pct_confirmados = 0
if not df_cal.empty:
    pct_confirmados = (df_cal["Estado"] == "CONFIRMADO CON CLIENTE").sum() / len(df_cal) * 100

# Health Score ponderado
score_cumpl  = min(cumplimiento, 100)
score_sla    = max(0, 100 - (vencidos_sla / max(total_tickets, 1) * 100) * 3)
score_conf   = pct_confirmados
health_score = int(score_cumpl * 0.5 + score_sla * 0.3 + score_conf * 0.2)

if health_score >= 80:
    health_color  = "#56d364"
    health_status = "OPERACIÓN SALUDABLE"
elif health_score >= 55:
    health_color  = "#f0c040"
    health_status = "ATENCIÓN REQUERIDA"
else:
    health_color  = "#F85149"
    health_status = "RIESGO OPERATIVO"

tecnicos_sobre100   = df[df["% Cumplimiento"] > 100]["Técnico"].tolist()
tecnicos_sin_agenda = df[df["Agenda semana pasada"] == 0]["Técnico"].tolist()

# ==========================================
# HEADER
# ==========================================
h1, h2 = st.columns([5, 2])
with h1:
    st.markdown(f"""
        <div style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:800;
                    color:#F0F6FC; letter-spacing:-0.5px; line-height:1;'>
            Cuadro de Mando Operativo
        </div>
        <div style='font-family:DM Mono,monospace; font-size:0.72rem; color:#4facfe;
                    letter-spacing:2px; margin-top:6px;'>
            {vista_label}
        </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown(f"""
        <div style='text-align:right; padding-top:8px;'>
            <span class='corte-badge'>CORTE: {fecha_corte_str.upper()}</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# HEALTH SCORE BANNER
# ==========================================
st.markdown(f"""
<div class="health-banner">
    <div>
        <div class="health-score-label">ÍNDICE DE SALUD OPERACIONAL</div>
        <div class="health-score-value" style="color:{health_color};">{health_score}<span style='font-size:1.5rem; color:#4B5563;'>/100</span></div>
        <div class="health-score-sub">{health_status} · Semana en curso</div>
    </div>
    <div style="display:flex; gap:60px; align-items:center;">
        <div style="text-align:center;">
            <div style='font-family:DM Mono,monospace; font-size:0.65rem; color:#4B5563; letter-spacing:1.5px; margin-bottom:4px;'>CUMPLIMIENTO</div>
            <div style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:700;
                        color:{"#56d364" if cumplimiento>=80 else "#f0c040" if cumplimiento>=50 else "#F85149"};'>
                {cumplimiento:.0f}%</div>
        </div>
        <div style="text-align:center;">
            <div style='font-family:DM Mono,monospace; font-size:0.65rem; color:#4B5563; letter-spacing:1.5px; margin-bottom:4px;'>SLA VENCIDOS</div>
            <div style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:700;
                        color:{"#F85149" if vencidos_sla>5 else "#f0c040" if vencidos_sla>0 else "#56d364"};'>
                {vencidos_sla}</div>
        </div>
        <div style="text-align:center;">
            <div style='font-family:DM Mono,monospace; font-size:0.65rem; color:#4B5563; letter-spacing:1.5px; margin-bottom:4px;'>CONFIRMADOS</div>
            <div style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:700;
                        color:{"#56d364" if pct_confirmados>=80 else "#f0c040" if pct_confirmados>=50 else "#F85149"};'>
                {pct_confirmados:.0f}%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Alertas
if tecnicos_sobre100:
    nombres = ", ".join([n.split()[0] for n in tecnicos_sobre100])
    st.markdown(f'<div class="alert-strip warn">⚠ CUMPLIMIENTO &gt;100% · <b>{nombres}</b> — Verificar visitas no agendadas o error de registro</div>', unsafe_allow_html=True)
if tecnicos_sin_agenda:
    nombres_sa = ", ".join([n.split()[0] for n in tecnicos_sin_agenda])
    st.markdown(f'<div class="alert-strip info">ℹ SIN AGENDA ASIGNADA · <b>{nombres_sa}</b> — Cumplimiento no calculable</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# KPI STRIP — 4 columnas
# ==========================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-icon">🎯</div>
        <div class="kpi-label">VISITAS REALIZADAS</div>
        <div class="kpi-value">{total_visitas}</div>
        <div class="kpi-delta" style="color:#4facfe;">de {total_agenda} planificadas</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">TOTAL FACTURADO</div>
        <div class="kpi-value" style="font-size:1.5rem;">${total_venta:,.0f}</div>
        <div class="kpi-delta" style="color:#56d364;">COP · semana en curso</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card gold">
        <div class="kpi-icon">🧾</div>
        <div class="kpi-label">TICKET PROMEDIO</div>
        <div class="kpi-value" style="font-size:1.5rem;">${ticket_prom:,.0f}</div>
        <div class="kpi-delta" style="color:#D29922;">COP por factura</div>
    </div>""", unsafe_allow_html=True)

with k4:
    gasto_color = "red" if total_gastos > total_venta * 0.3 else "blue"
    st.markdown(f"""
    <div class="kpi-card {gasto_color}">
        <div class="kpi-icon">📦</div>
        <div class="kpi-label">GASTOS OPERATIVOS</div>
        <div class="kpi-value" style="font-size:1.5rem;">${total_gastos:,.0f}</div>
        <div class="kpi-delta" style="color:#8B949E;">COP · período</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# FILA 2: CUMPLIMIENTO + TICKETS
# ==========================================
st.markdown('<div class="section-header">RENDIMIENTO TÉCNICOS · TICKETS</div>', unsafe_allow_html=True)

col_bar, col_tix = st.columns([3, 1])

with col_bar:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-title">Cumplimiento por Técnico</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-sub">VISITAS REALES VS PLANIFICADAS · META 80%</div>', unsafe_allow_html=True)

    df_bar = df[df["Agenda semana pasada"] > 0].copy()
    df_bar = df_bar.sort_values("% Cumplimiento", ascending=True)

    if not df_bar.empty:
        colors = [
            "#56d364" if v >= 80 else "#f0c040" if v >= 50 else "#F85149"
            for v in df_bar["% Cumplimiento"]
        ]
        df_bar["Nombre_corto"] = df_bar["Técnico"].apply(
            lambda x: " ".join(x.split()[:2]) if len(x.split()) >= 2 else x
        )

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df_bar["% Cumplimiento"],
            y=df_bar["Nombre_corto"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0), opacity=0.85),
            text=[f"{v:.0f}%" for v in df_bar["% Cumplimiento"]],
            textposition="outside",
            textfont=dict(family="DM Mono, monospace", size=11, color="#C9D1D9"),
            hovertemplate="<b>%{y}</b><br>Cumplimiento: %{x:.1f}%<extra></extra>",
        ))
        fig_bar.add_vline(
            x=80, line_dash="dash", line_color="rgba(79,172,254,0.5)", line_width=1.5,
            annotation_text="META 80%", annotation_font_size=10,
            annotation_font_color="#4facfe", annotation_position="top right"
        )
        fig_bar.add_vrect(x0=80, x1=130, fillcolor="rgba(46,160,67,0.04)", line_width=0)

        style_fig(fig_bar,
                  xaxis=dict(range=[0, max(130, df_bar["% Cumplimiento"].max() + 15)],
                             ticksuffix="%", showgrid=True),
                  yaxis=dict(showgrid=False),
                  height=max(220, len(df_bar) * 48),
                  bargap=0.35, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Sin datos de cumplimiento para mostrar.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_tix:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-title">Tickets · Backlog</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-sub">ZOHO DESK · ESTADO ACTUAL</div>', unsafe_allow_html=True)

    estilos_chip = {
        "VENCIDOS (SLA)":  ("danger",  "⚠", "#F85149", "Atención crítica"),
        "SIN CIERRE":      ("warning", "⌛", "#D29922", "Pendientes flujo"),
        "NUEVOS/ABIERTOS": ("info",    "✉", "#58A6FF", "Carga operativa"),
    }
    for _, row in df_tickets.iterrows():
        estado   = row["Estado"]
        cantidad = int(row["Cantidad"])
        if estado in estilos_chip:
            cls, icono, color, label = estilos_chip[estado]
            st.markdown(f"""
            <div class="ticket-chip {cls}">
                <div>
                    <div class="chip-label" style="color:{color};">{icono} {estado}</div>
                    <div class="chip-sub">{label}</div>
                </div>
                <div class="chip-value" style="color:{color};">{cantidad}</div>
            </div>""", unsafe_allow_html=True)

    fig_pie = px.pie(
        df_tickets, values="Cantidad", names="Estado", hole=0.65,
        color="Estado",
        color_discrete_map={
            "VENCIDOS (SLA)":  "#F85149",
            "SIN CIERRE":      "#D29922",
            "NUEVOS/ABIERTOS": "#58A6FF"
        }
    )
    fig_pie.update_traces(textinfo="none",
                          hovertemplate="<b>%{label}</b><br>%{value} tickets<extra></extra>")
    style_fig(fig_pie, height=160, showlegend=False,
              margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# FILA 3: VENTAS DIARIAS + SEGMENTO
# ==========================================
st.markdown('<div class="section-header">ANÁLISIS DE VENTAS</div>', unsafe_allow_html=True)

col_line, col_seg = st.columns([3, 2])

with col_line:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-title">Ventas Diarias — Semana en Curso</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-sub">COP · FACTURAS POSITIVAS ÚNICAMENTE</div>', unsafe_allow_html=True)

    df_daily = df_v_pos.groupby("Fecha")["Venta_num"].sum().reset_index().sort_values("Fecha")

    if not df_daily.empty:
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily["Fecha"], y=df_daily["Venta_num"],
            mode="lines+markers",
            line=dict(color="#4facfe", width=2.5, shape="spline"),
            marker=dict(size=7, color="#4facfe", line=dict(width=2, color="#080A0F")),
            fill="tozeroy", fillcolor="rgba(79,172,254,0.07)",
            hovertemplate="<b>%{x|%d %b}</b><br>$%{y:,.0f} COP<extra></extra>",
            name="Ventas"
        ))
        promedio = df_daily["Venta_num"].mean()
        fig_line.add_hline(
            y=promedio, line_dash="dot",
            line_color="rgba(240,192,64,0.4)", line_width=1.5,
            annotation_text=f"  Prom ${promedio:,.0f}",
            annotation_font_size=10, annotation_font_color="#f0c040"
        )
        style_fig(fig_line,
                  xaxis=dict(tickformat="%d %b", showgrid=False),
                  yaxis=dict(tickprefix="$", tickformat=",.0f"),
                  height=260, showlegend=False)
        st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Sin datos de ventas disponibles.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_seg:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-title">Ventas por Segmento</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box-sub">DISTRIBUCIÓN DEL PERÍODO · COP</div>', unsafe_allow_html=True)

    if not df_v_pos.empty and "Segmento" in df_v_pos.columns:
        df_seg = df_v_pos.groupby("Segmento")["Venta_num"].sum().reset_index()
        df_seg = df_seg.sort_values("Venta_num", ascending=True)
        palette = ["#4facfe", "#00f2fe", "#56d364", "#f0c040", "#D29922", "#ff7b72"]

        fig_seg = go.Figure(go.Bar(
            x=df_seg["Venta_num"], y=df_seg["Segmento"],
            orientation="h",
            marker=dict(color=palette[:len(df_seg)], opacity=0.85, line=dict(width=0)),
            text=[f"${v:,.0f}" for v in df_seg["Venta_num"]],
            textposition="outside",
            textfont=dict(family="DM Mono, monospace", size=10, color="#8B949E"),
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f} COP<extra></extra>",
        ))
        style_fig(fig_seg,
                  xaxis=dict(tickprefix="$", tickformat=",.0f", showgrid=True),
                  yaxis=dict(showgrid=False),
                  height=260, bargap=0.35, showlegend=False)
        st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Sin datos de segmento disponibles.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# FILA 4: CALENDARIO VISUAL
# ==========================================
st.markdown('<div class="section-header">CALENDARIO OPERATIVO</div>', unsafe_allow_html=True)

if df_cal.empty:
    st.info("Sin agendamientos para el técnico seleccionado.")
else:
    # Mini KPIs de calendario
    c1, c2, c3 = st.columns(3)
    servicios_por_tec = df_cal.groupby("Técnico").size()

    with c1:
        tec_mas       = servicios_por_tec.idxmax()
        tec_mas_count = int(servicios_por_tec.max())
        nombre_corto  = " ".join(tec_mas.split()[:2]) if len(tec_mas.split()) >= 2 else tec_mas
        st.markdown(f"""
        <div class="kpi-card blue" style="padding:16px 20px;">
            <div class="kpi-label">MÁS SERVICIOS</div>
            <div class="kpi-value" style="font-size:1.1rem;">{nombre_corto}</div>
            <div class="kpi-delta" style="color:#4facfe;">{tec_mas_count} servicios agendados</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        tec_menos       = servicios_por_tec.idxmin()
        tec_menos_count = int(servicios_por_tec.min())
        nombre_corto2   = " ".join(tec_menos.split()[:2]) if len(tec_menos.split()) >= 2 else tec_menos
        st.markdown(f"""
        <div class="kpi-card gold" style="padding:16px 20px;">
            <div class="kpi-label">MENOS SERVICIOS</div>
            <div class="kpi-value" style="font-size:1.1rem;">{nombre_corto2}</div>
            <div class="kpi-delta" style="color:#D29922;">{tec_menos_count} servicio(s)</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        color_pct = "#56d364" if pct_confirmados >= 80 else ("#f0c040" if pct_confirmados >= 50 else "#F85149")
        card_cls  = "green" if pct_confirmados >= 80 else ("gold" if pct_confirmados >= 50 else "red")
        st.markdown(f"""
        <div class="kpi-card {card_cls}" style="padding:16px 20px;">
            <div class="kpi-label">CONFIRMADOS</div>
            <div class="kpi-value" style="color:{color_pct};">{pct_confirmados:.1f}%</div>
            <div class="kpi-delta" style="color:#8B949E;">del total de la agenda</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Calendario visual con pills de colores
    pill_class = {
        "CONFIRMADO CON CLIENTE":    "conf",
        "POR CONFIRMAR CON CLIENTE": "pconf",
        "PENDIENTE PROGRAMAR":       "pend",
        "REPROGRAMADO":              "reprog",
        "EJECUTADO":                 "ejec",
    }
    df_cal_v = df_cal.copy()
    df_cal_v["Fecha_str"] = df_cal_v["Fecha"].dt.strftime("%a %d/%m")
    df_cal_v["pill_cls"]  = df_cal_v["Estado"].map(pill_class).fillna("pend")
    df_cal_v["Cliente_s"] = df_cal_v["Cliente"].str.title().str[:20]

    tecnicos_cal = sorted(df_cal_v["Técnico"].unique())
    fechas_cal   = sorted(df_cal_v["Fecha_str"].unique())

    thead_cells = "".join([
        f"<th style='font-family:DM Mono,monospace;font-size:0.65rem;color:#4B5563;"
        f"padding:8px 12px;letter-spacing:1px;text-align:left;"
        f"border-bottom:1px solid #1C2333;white-space:nowrap;'>{f}</th>"
        for f in fechas_cal
    ])

    rows_html = ""
    for tec in tecnicos_cal:
        nombre_t = " ".join(tec.split()[:2]) if len(tec.split()) >= 2 else tec
        row_cells = (
            f"<td style='font-family:DM Mono,monospace;font-size:0.7rem;color:#8B949E;"
            f"padding:10px 12px;white-space:nowrap;border-bottom:1px solid #0D1117;"
            f"min-width:120px;'>{nombre_t}</td>"
        )
        for fecha in fechas_cal:
            filas = df_cal_v[(df_cal_v["Técnico"] == tec) & (df_cal_v["Fecha_str"] == fecha)]
            if filas.empty:
                cell_content = "<span style='color:#1C2333;font-size:0.7rem;'>—</span>"
            else:
                cell_content = "".join([
                    f"<span class='cal-pill {r.pill_cls}'>{r.Cliente_s}</span>"
                    for _, r in filas.iterrows()
                ])
            row_cells += (
                f"<td style='padding:6px 10px;border-bottom:1px solid #0D1117;vertical-align:top;'>"
                f"{cell_content}</td>"
            )
        rows_html += f"<tr>{row_cells}</tr>"

    st.markdown(f"""
    <div style='background:#0D1117;border:1px solid #1C2333;border-radius:14px;overflow-x:auto;padding:4px;'>
        <table style='width:100%;border-collapse:collapse;'>
            <thead>
                <tr>
                    <th style='font-family:DM Mono,monospace;font-size:0.65rem;color:#4B5563;
                               padding:8px 12px;letter-spacing:1px;text-align:left;
                               border-bottom:1px solid #1C2333;min-width:120px;'>TÉCNICO</th>
                    {thead_cells}
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# DETALLE COLAPSABLE (tablas crudas)
# ==========================================
with st.expander("📋  Ver detalle completo — Operaciones · Facturas", expanded=False):
    det1, det2 = st.tabs(["Operaciones por Técnico", "Detalle de Facturas"])

    with det1:
        df_display = df[[
            "Técnico", "Visitas registradas", "Agenda semana pasada",
            "% Cumplimiento", "Gastos", "Cantidad de ventas reportada",
            "Servicios agendados esta semana"
        ]].copy()
        st.dataframe(
            df_display,
            column_config={
                "Técnico": st.column_config.TextColumn("Técnico Asignado", width="medium"),
                "Visitas registradas": st.column_config.NumberColumn("Real", format="%d"),
                "Agenda semana pasada": st.column_config.NumberColumn("Plan", format="%d"),
                "% Cumplimiento": st.column_config.ProgressColumn(
                    "Cumplimiento", format="%.1f%%", min_value=0, max_value=100),
                "Gastos": st.column_config.NumberColumn("Gastos (COP)", format="$ %d"),
                "Cantidad de ventas reportada": st.column_config.NumberColumn("Ventas", format="%d"),
                "Servicios agendados esta semana": st.column_config.NumberColumn("Próx. Semana", format="%d"),
            },
            hide_index=True, use_container_width=True,
            height=(len(df_display) * 35 + 38)
        )

    with det2:
        df_v_disp = df_v_pos[[
            "Factura periodo", "Fecha", "Cliente", "Segmento", "Ciudad", "Venta_num"
        ]].sort_values("Fecha", ascending=False)
        st.dataframe(
            df_v_disp,
            column_config={
                "Factura periodo": st.column_config.TextColumn("Factura", width="small"),
                "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
                "Cliente": st.column_config.TextColumn("Cliente", width="large"),
                "Segmento": st.column_config.TextColumn("Segmento"),
                "Ciudad": st.column_config.TextColumn("Ciudad"),
                "Venta_num": st.column_config.NumberColumn("Valor (COP)", format="$ %,.0f"),
            },
            hide_index=True, use_container_width=True,
            height=(len(df_v_disp) * 35 + 38)
        )
        nc = df_v_ops[df_v_ops["Venta_num"] < 0]
        if not nc.empty:
            total_nc = nc["Venta_num"].sum()
            st.caption(f"ℹ️ Se excluyeron {len(nc)} nota(s) crédito por ${total_nc:,.0f} COP.")