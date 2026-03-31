import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from pathlib import Path
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    layout="wide",
    page_title="GYM Shop | Dashboard Ejecutivo",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; font-weight: 600; }

    .kpi-card {
        background: linear-gradient(145deg, #1A1C23 0%, #121418 100%);
        border: 1px solid #2D303E;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.2s ease-in-out;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: #4facfe; }
    .kpi-title { color: #8B949E; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .kpi-value { color: #FFFFFF; font-size: 2.2rem; font-weight: 700; margin-bottom: 5px; }
    .kpi-sub   { color: #8B949E; font-size: 0.85rem; }

    .ticket-card { border-radius: 12px; padding: 20px; text-align: center; font-weight: bold; }
    .ticket-card.danger  { background-color: rgba(248,81,73,0.1);  border: 1px solid #F85149; }
    .ticket-card.warning { background-color: rgba(210,153,34,0.1); border: 1px solid #D29922; }
    .ticket-card.info    { background-color: rgba(88,166,255,0.1); border: 1px solid #58A6FF; }
    .t-val { font-size: 3.5rem; line-height: 1; margin: 10px 0; }

    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; border-radius: 4px 4px 0 0; padding: 10px; }
    .stTabs [aria-selected="true"] { color: #4facfe !important; border-bottom: 2px solid #4facfe !important; }

    .alert-warning {
        background-color: rgba(210,153,34,0.1);
        border: 1px solid #D29922;
        border-radius: 8px;
        padding: 8px 14px;
        color: #D29922;
        font-size: 0.85rem;
        margin-top: 6px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================
# CARGA DE DATOS — DESDE ARCHIVOS CSV
# ==========================================
# Resolución de ruta compatible con local y Streamlit Cloud
# En Streamlit Cloud el app corre desde el root del repo, no desde la carpeta del archivo
_THIS_FILE = Path(__file__).resolve()
_CANDIDATES = [
    Path(os.getcwd()),                       # raiz del repo (Streamlit Cloud, CSV sueltos)
    _THIS_FILE.parent,                       # mismo directorio que dashboard.py
    Path(os.getcwd()) / "data",             # subcarpeta data/ en raiz
    _THIS_FILE.parent / "data",             # subcarpeta data/ junto al script
]
DATA_DIR = next(
    (p for p in _CANDIDATES if (p / "operaciones.csv").exists()),
    Path(os.getcwd())
)

@st.cache_data(ttl=300)  # Refresca cada 5 minutos si el archivo cambia
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

    # Ventas semanales
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

    # Calcular % de visitas vs agenda (evitar división por cero)
    df_ops["% Cumplimiento"] = df_ops.apply(
        lambda r: (r["Visitas registradas"] / r["Agenda semana pasada"] * 100)
        if r["Agenda semana pasada"] > 0 else None,
        axis=1
    )
    return df_ops, df_cal, df_tickets, df_ventas

df_master, df_cal_master, df_tickets, df_ventas = load_data()

# Fecha de corte dinámica: último lunes de los datos del calendario
fecha_corte = df_cal_master["Fecha"].max()
fecha_corte_str = fecha_corte.strftime("%-d de %B, %Y") if hasattr(fecha_corte, 'strftime') else str(fecha_corte)


# ==========================================
# SIDEBAR Y FILTROS
# ==========================================
with st.sidebar:
    st.markdown("### GYM Shop <span style='color:#F85149;'>®</span>", unsafe_allow_html=True)
    st.caption("Panel de Control Gerencial")
    st.markdown("---")
    st.markdown("**Filtros Operativos**")

    lista_tecnicos = ["Ver Todos (Visión Global)"] + sorted(df_master["Técnico"].unique().tolist())
    tec_seleccionado = st.selectbox("👨‍🔧 Seleccionar Técnico:", lista_tecnicos)

    st.markdown("---")
    if st.button("🔄 Recargar datos"):
        st.cache_data.clear()
        st.rerun()

    st.caption("Desarrollado por Techforce")

# Aplicar filtro
if tec_seleccionado == "Ver Todos (Visión Global)":
    df = df_master.copy()
    df_cal = df_cal_master.copy()
    vista_actual = "Visión Global (Toda la compañía)"
else:
    df = df_master[df_master["Técnico"] == tec_seleccionado].copy()
    df_cal = df_cal_master[df_cal_master["Técnico"] == tec_seleccionado].copy()
    vista_actual = f"Rendimiento de: {tec_seleccionado}"


# ==========================================
# MÉTRICAS CALCULADAS (sin hardcoding)
# ==========================================
total_visitas_real = int(df["Visitas registradas"].sum())
total_gastos    = float(df["Gastos"].sum())
total_visitas   = int(df["Visitas registradas"].sum())
total_agenda    = int(df["Agenda semana pasada"].sum())
cumplimiento    = (total_visitas / total_agenda * 100) if total_agenda > 0 else 0

# Técnicos con cumplimiento > 100% (para alerta)
tecnicos_sobre100 = df[df["% Cumplimiento"] > 100]["Técnico"].tolist()

# Técnicos sin agenda asignada
tecnicos_sin_agenda = df[df["Agenda semana pasada"] == 0]["Técnico"].tolist()


# ==========================================
# CABECERA
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("<h2>Cuadro de Mando Operativo Semanal</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#4facfe; font-weight:bold;'>{vista_actual}</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown(
        f"<div style='text-align:right; color:#8B949E; margin-top:15px;'>"
        f"Corte: <b>{fecha_corte_str}</b></div>",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. VISIÓN GENERAL Y KPIs",
    "🎫 2. SOPORTE Y TICKETS (DESK)",
    "📅 3. AGENDA Y CALENDARIO",
    "💰 4. VENTA SEMANAL"
])


# ------------------------------------------
# TAB 1: KPIs
# ------------------------------------------
with tab1:
    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Visitas Realizadas</div>
            <div class="kpi-value">{total_visitas_real}</div>
            <div class="kpi-sub">Suma columna Real del período</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Gastos Operativos (COP)</div>
            <div class="kpi-value">${total_gastos:,.0f}</div>
            <div class="kpi-sub">Gastos reportados del período</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        color_cum = "#2EA043" if cumplimiento >= 80 else ("#D29922" if cumplimiento >= 50 else "#F85149")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">% Cumplimiento Global</div>
            <div class="kpi-value" style="color:{color_cum};">{cumplimiento:.1f}%</div>
            <div class="kpi-sub">Visitas reales vs planificadas</div>
        </div>""", unsafe_allow_html=True)

    # Alertas calculadas — no hardcodeadas
    if tecnicos_sobre100:
        nombres = ", ".join([n.split()[0] for n in tecnicos_sobre100])
        st.markdown(
            f'<div class="alert-warning">⚠️ Cumplimiento superior al 100%: <b>{nombres}</b> — '
            f'Verificar si hay visitas no agendadas o error de registro.</div>',
            unsafe_allow_html=True
        )

    if tecnicos_sin_agenda:
        nombres_sa = ", ".join([n.split()[0] for n in tecnicos_sin_agenda])
        st.markdown(
            f'<div class="alert-warning" style="border-color:#58A6FF; color:#58A6FF; background:rgba(88,166,255,0.07);">'
            f'ℹ️ Sin agenda asignada: <b>{nombres_sa}</b> — No se calcula cumplimiento para estos técnicos.</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 📋 Detalle Operativo")

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
                "Cumplimiento",
                help="N/A = sin agenda asignada. >100% = visitas superaron el plan.",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            ),
            "Gastos": st.column_config.NumberColumn("Gastos (COP)", format="$ %d"),
            "Cantidad de ventas reportada": st.column_config.NumberColumn("Ventas", format="%d"),
            "Servicios agendados esta semana": st.column_config.NumberColumn("Agenda próx. semana", format="%d"),
        },
        hide_index=True,
        use_container_width=True,
        height=(len(df_display) * 35 + 38)
    )


# ------------------------------------------
# TAB 2: TICKETS (desde CSV)
# ------------------------------------------
with tab2:
    st.markdown("### Estado Actual del Backlog (Zoho Desk)")
    st.caption("Datos globales de la cola de servicio. Actualizar en `data/tickets.csv`.")

    # Mapeo de estilos por estado
    estilos = {
        "VENCIDOS (SLA)":   ("danger",  "⚠️", "#F85149", "Atención Crítica"),
        "SIN CIERRE":       ("warning", "⌛", "#D29922", "Pendientes de Flujo"),
        "NUEVOS/ABIERTOS":  ("info",    "✉️", "#58A6FF", "Carga Operativa"),
    }

    cols_tickets = st.columns([1, 1, 1, 1.5])

    for i, (_, row) in enumerate(df_tickets.iterrows()):
        estado = row["Estado"]
        cantidad = int(row["Cantidad"])
        if estado in estilos:
            cls, icono, color, label = estilos[estado]
            with cols_tickets[i]:
                st.markdown(
                    f'<div class="ticket-card {cls}">'
                    f'<div style="color:{color};">{icono} {estado}</div>'
                    f'<div class="t-val" style="color:{color};">{cantidad}</div>'
                    f'{label}</div>',
                    unsafe_allow_html=True
                )

    with cols_tickets[3]:
        fig_pie = px.pie(
            df_tickets,
            values="Cantidad",
            names="Estado",
            hole=0.6,
            color="Estado",
            color_discrete_map={
                "VENCIDOS (SLA)":  "#F85149",
                "SIN CIERRE":      "#D29922",
                "NUEVOS/ABIERTOS": "#58A6FF"
            }
        )
        fig_pie.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=0, b=0, l=0, r=0),
            height=200
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# ------------------------------------------
# TAB 3: AGENDA Y CALENDARIO (desde CSV)
# ------------------------------------------
with tab3:
    if df_cal.empty:
        st.info(
            "No hay agendamientos para el técnico seleccionado. "
            "Verifica el archivo `data/calendario.csv`."
        )
    else:
        st.markdown("#### Matriz de Programación")

        state_icons = {
            "CONFIRMADO CON CLIENTE":    "🟢 Conf.",
            "POR CONFIRMAR CON CLIENTE": "🟠 Por Conf.",
            "PENDIENTE PROGRAMAR":       "🔵 Pend.",
            "REPROGRAMADO":              "🔴 Reprog.",
            "EJECUTADO":                 "✅ Ejec.",
        }

        df_cal_view = df_cal.copy()
        df_cal_view["Icono"] = df_cal_view["Estado"].map(state_icons).fillna(df_cal_view["Estado"])
        df_cal_view["Fecha_str"] = df_cal_view["Fecha"].dt.strftime("%d/%m")

        summary_mat = (
            df_cal_view
            .groupby(["Técnico", "Fecha_str", "Icono"])
            .size()
            .reset_index(name="count")
        )
        summary_mat["Tag"] = summary_mat["count"].astype(str) + " " + summary_mat["Icono"]

        table_data = (
            summary_mat
            .groupby(["Técnico", "Fecha_str"])["Tag"]
            .apply(lambda x: " | ".join(x))
            .reset_index()
        )

        try:
            pivot_table = (
                table_data
                .pivot_table(index="Técnico", columns="Fecha_str", values="Tag", aggfunc="first")
                .fillna("-")
                .reset_index()
            )
            n_rows = len(pivot_table)
            st.dataframe(pivot_table, hide_index=True, use_container_width=True, height=(n_rows * 35 + 38))
        except Exception as e:
            st.error(f"No se pudo construir la matriz de programación: {e}")


# ------------------------------------------
# TAB 4: VENTA SEMANAL
# ------------------------------------------
with tab4:
    # Filtrar ventas solo positivas (excluir notas crédito)
    df_v = df_ventas[df_ventas["Venta_num"] > 0].copy()

    total_venta      = df_v["Venta_num"].sum()
    num_facturas     = len(df_v)
    ticket_promedio  = df_v["Venta_num"].mean()
    num_clientes     = df_v["Cliente"].nunique()
    ciudad_top       = df_v.groupby("Ciudad")["Venta_num"].sum().idxmax()
    segmento_top     = df_v.groupby("Segmento")["Venta_num"].sum().idxmax()

    # KPIs
    v1, v2, v3 = st.columns(3)
    with v1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Facturado</div>
            <div class="kpi-value" style="font-size:1.7rem;">${total_venta:,.0f}</div>
            <div class="kpi-sub">COP — semana en curso</div>
        </div>""", unsafe_allow_html=True)
    with v2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ticket Promedio</div>
            <div class="kpi-value" style="font-size:1.7rem;">${ticket_promedio:,.0f}</div>
            <div class="kpi-sub">COP por factura</div>
        </div>""", unsafe_allow_html=True)
    with v3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Top Segmento</div>
            <div class="kpi-value" style="font-size:1.4rem;">{segmento_top}</div>
            <div class="kpi-sub">Mayor volumen · {ciudad_top}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 📋 Detalle de Facturas")
    df_v_display = df_v[[
        "Factura periodo", "Fecha", "Cliente", "Segmento", "Ciudad", "Venta_num"
    ]].copy()
    df_v_display = df_v_display.sort_values("Fecha", ascending=False)

    st.dataframe(
        df_v_display,
        column_config={
            "Factura periodo": st.column_config.TextColumn("Factura", width="small"),
            "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "Cliente": st.column_config.TextColumn("Cliente", width="large"),
            "Segmento": st.column_config.TextColumn("Segmento"),
            "Ciudad": st.column_config.TextColumn("Ciudad"),
            "Venta_num": st.column_config.NumberColumn("Valor (COP)", format="$ %,.0f"),
        },
        hide_index=True,
        use_container_width=True,
        height=(len(df_v_display) * 35 + 38)
    )

    # Nota sobre notas crédito excluidas
    nc = df_ventas[df_ventas["Venta_num"] < 0]
    if not nc.empty:
        total_nc = nc["Venta_num"].sum()
        st.caption(f"ℹ️ Se excluyeron {len(nc)} nota(s) crédito por un total de ${total_nc:,.0f} COP. No afectan el total facturado.")