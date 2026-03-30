import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re

st.set_page_config(layout="wide", page_title="Cuadro Técnicos Semanal")

# ── DATOS ────────────────────────────────────────────────────────────────────
raw_data = {
    'Técnico': [
        'CONTRERAS CORZO JAVIER ALEXANDER', 'JESUS ARMANDO JOYA DIAZ',
        'VARGAS RESTREPO ANDRES FELIPE', 'ACOSTA MARTINEZ OSMAN OMAR',
        'RONCANCIO BELTRAN WILSON EMEIRO', 'LOPEZ GIRALDO JAMIR',
        'GOMEZ CARDENAS MAURICIO', 'RODRIGUEZ CESAR AUGUSTO',
        'CARDOZO CASTRO EDGAR GIOVANNY', 'JIMENEZ VELOZA LUCINIO IVAN',
        'JAVIER ESTIVEN MORA', 'VANEGAS YONI ALBEIRO',
        'ROMERO SERRANO LUIS MIGUEL', 'PAJARO ESCORCIA MARTIN',
        'RIOS ARANGO ADRIAN ALONSO'
    ],
    'Visitas registradas':     [5, 1, 2, 0, 0, 1, 2, 3, 4, 2, 1, 0, 2, 2, 1],
    'Agenda semana pasada':    [6, 4, 2, 2, 5, 5, 6, 7, 3, 5, 6, 4, 4, 4, 2],
    '% de visitas vs agenda':  [
        '83.3 %', '25.0 %', '100.0 %', '0.0 %', '0.0 %', '20.0 %',
        '33.3 %', '42.9 %', '133.3 %', '40.0 %', '16.7 %', '0.0 %',
        '50.0 %', '50.0 %', '50.0 %'
    ],
    'Gastos': [
        '590.650 COP', '0 COP', '86.900 COP', '0 COP', '0 COP', '30.000 COP',
        '36.400 COP', '0 COP', '51.000 COP', '45.000 COP', '37.100 COP',
        '0 COP', '0 COP', '0 COP', '18.000 COP'
    ],
    'Cantidad de ventas reportada':    [4, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 1],
    'Servicios agendados esta semana': [2, 4, 4, 4, 1, 4, 3, 3, 1, 3, 1, 0, 0, 0, 0]
}

df = pd.DataFrame(raw_data)

# ── FUNCIONES DE LIMPIEZA (refactorizadas) ───────────────────────────────────
def clean_cop(val):
    """Extrae el valor numérico de un string de moneda como '590.650 COP'."""
    if not isinstance(val, str):
        return int(val) if val else 0
    digits = re.sub(r'[^\d]', '', val)
    return int(digits) if digits else 0

def shorten_tech_name(full_name):
    """Abrevia un nombre: 'CONTRERAS CORZO JAVIER' → 'CONTRERAS C.'"""
    if not isinstance(full_name, str) or not full_name.strip():
        return "—"
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0].capitalize()
    return f"{parts[0].capitalize()} {parts[1][0]}."

# ── PREPROCESAMIENTO ──────────────────────────────────────────────────────────
df['Gastos_num']        = df['Gastos'].apply(clean_cop)
df['% Cumplimiento_pct'] = df['% de visitas vs agenda'].str.replace(' %', '').astype(float)
df['Técnico_Abrev']     = df['Técnico'].apply(shorten_tech_name)

# ── MÉTRICAS GLOBALES (sobre datos completos) ─────────────────────────────────
total_ventas         = df['Cantidad de ventas reportada'].sum()
total_gastos         = df['Gastos_num'].sum()
total_visitas        = df['Visitas registradas'].sum()
total_agenda         = df['Agenda semana pasada'].sum()
cumplimiento_promedio = (total_visitas / total_agenda * 100) if total_agenda > 0 else 0

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    body, .stApp { background-color: #111 !important; color: #f0f0f0 !important; }
    h1, h2, h3, h4, p, label { color: white !important; }

    .sec-hdr {
        color: white; font-size: 12px; font-weight: 700; letter-spacing: 1.5px;
        text-transform: uppercase; padding-bottom: 8px;
        border-bottom: 1px solid #2a2a2a; margin-bottom: 14px;
    }
    .kpi-card {
        background: #1c1c1c; border: 1px solid #2a2a2a;
        border-radius: 10px; padding: 14px 16px; margin-bottom: 12px;
        display: flex; align-items: center; gap: 14px;
    }
    .kpi-icon  { font-size: 28px; flex-shrink: 0; }
    .kpi-inner { display: flex; flex-direction: column; }
    .kpi-label { font-size: 9px; color: #888; letter-spacing: 1px; text-transform: uppercase; }
    .kpi-value { font-size: 26px; font-weight: 700; color: white; line-height: 1.15; }
    .kpi-value-sm { font-size: 18px; font-weight: 700; color: white; line-height: 1.15; }
    .trend-up   { font-size: 10px; color: #50e3c2; }
    .trend-down { font-size: 10px; color: #ff6b6b; }

    .tkt-card {
        background: #1a1a1a; border-radius: 10px; padding: 18px 12px;
        text-align: center; display: flex; flex-direction: column;
        align-items: center; gap: 4px; height: 100%;
    }
    .tkt-card.red  { border: 2px solid #ff4b4b; }
    .tkt-card.orng { border: 2px solid #ff9f43; }
    .tkt-card.blue { border: 2px solid #3b82f6; }
    .tkt-lbl  { font-size: 12px; font-weight: 700; letter-spacing: 1px; }
    .tkt-sub  { font-size: 9px;  color: #888; }
    .tkt-num  { font-size: 52px; font-weight: 800; line-height: 1; margin: 6px 0; }
    .tkt-foot { font-size: 9px;  font-weight: 700; letter-spacing: 0.5px; }

    .panel   { background: #1a1a1a; border-radius: 10px; padding: 16px; margin-bottom: 14px; }
    .divider { border: none; border-top: 1px solid #2a2a2a; margin: 4px 0 14px; }
    .footer-txt { color: #444; font-size: 9px; text-align: center;
                  padding: 10px 0; border-top: 1px solid #1e1e1e; }

    /* Ocultar borde blanco del dataframe */
    .stDataFrame { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
hdr1, hdr2, hdr3 = st.columns([1, 4, 2])

with hdr1:
    st.markdown("""
        <div style="color:white;font-weight:800;font-size:22px;line-height:1;">
            GYM<span style="font-size:8px;vertical-align:super;color:#ff4b4b;">®</span>
        </div>
        <div style="color:#888;font-size:8px;margin-bottom:4px;">Bienestar, Salud & Felicidad</div>
        <div style="color:white;font-size:8px;line-height:1.4;">
            CON MÁS DE<br>
            <span style="font-size:14px;font-weight:800;">30 AÑOS</span><br>
            TRAYECTORIA
        </div>
    """, unsafe_allow_html=True)

with hdr2:
    st.markdown(
        '<h1 style="text-align:center;font-size:28px;letter-spacing:2px;margin:0;">'
        'CUADRO TÉCNICOS SEMANAL</h1>',
        unsafe_allow_html=True
    )

with hdr3:
    st.markdown('<div style="text-align:right;color:#666;font-size:11px;margin-bottom:6px;">1 DE ABRIL, 2026</div>', unsafe_allow_html=True)
    fc1, fc2 = st.columns(2)
    with fc1:
        opciones = ["Todos"] + sorted(df['Técnico'].apply(shorten_tech_name).tolist())
        st.selectbox("Técnico", opciones, key="tech_filter", label_visibility="collapsed")
    with fc2:
        st.date_input("Fecha", label_visibility="collapsed")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── APLICAR FILTRO ────────────────────────────────────────────────────────────
sel = st.session_state.get("tech_filter", "Todos")
if sel and sel != "Todos":
    df_f = df[df['Técnico_Abrev'] == sel].copy()
else:
    df_f = df.copy()

# ══════════════════════════════════════════════════════════════
# FILA 1: KPIs  |  TABLA  |  GRÁFICO DE BARRAS
# ══════════════════════════════════════════════════════════════
col_kpi, col_table, col_chart = st.columns([1, 3, 2], gap="medium")

# ── KPIs ──────────────────────────────────────────────────────
with col_kpi:
    st.markdown('<div class="sec-hdr">📋 Resumen Técnicos</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💳</div>
            <div class="kpi-inner">
                <div class="kpi-label">Total Ventas Reportadas</div>
                <div class="kpi-value">{total_ventas}</div>
                <div class="trend-up">📈 +12% vs. mes anterior</div>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-inner">
                <div class="kpi-label">Total Gastos Operativos</div>
                <div class="kpi-value-sm">COP {total_gastos:,.0f}</div>
                <div class="trend-down">📉 -5% vs. mes anterior</div>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-inner">
                <div class="kpi-label">% Cumplimiento Promedio (Vs Agenda)</div>
                <div class="kpi-value">{cumplimiento_promedio:.1f}%</div>
                <div class="trend-up">📈 +3.1% vs. mes anterior</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── TABLA CON BARRA DE PROGRESO ───────────────────────────────
with col_table:
    st.markdown('<div class="sec-hdr">📊 Detalle de Operación por Técnico</div>', unsafe_allow_html=True)

    df_display = df_f[[
        'Técnico_Abrev', 'Visitas registradas', 'Agenda semana pasada',
        '% Cumplimiento_pct', 'Gastos_num',
        'Cantidad de ventas reportada', 'Servicios agendados esta semana'
    ]].copy()
    df_display.columns = [
        'Técnico', 'Visitas', 'Agenda',
        '% Cumplimiento', 'Gastos (COP)', 'Ventas', 'Agendadas S.F.'
    ]

    st.dataframe(
        df_display,
        column_config={
            '% Cumplimiento': st.column_config.ProgressColumn(
                '% Cumplimiento %',
                format='%.1f%%',
                min_value=0,
                max_value=150,
            ),
            'Gastos (COP)': st.column_config.NumberColumn(
                'Gastos (COP)',
                format='%d',
            ),
        },
        use_container_width=True,
        hide_index=True,
        height=380,
    )

# ── GRÁFICO DE BARRAS ─────────────────────────────────────────
with col_chart:
    st.markdown('<div class="sec-hdr">📊 Comparativa: Visitas Reales vs. Agendadas por Técnico</div>', unsafe_allow_html=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_f['Técnico_Abrev'], y=df_f['Visitas registradas'],
        name='Visitas Reales', marker_color='white', offsetgroup=0
    ))
    fig_bar.add_trace(go.Bar(
        x=df_f['Técnico_Abrev'], y=df_f['Agenda semana pasada'],
        name='Agenda Planificada', marker_color='#555555', offsetgroup=1
    ))
    fig_bar.update_layout(
        paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a',
        margin=dict(l=8, r=8, t=10, b=80),
        legend=dict(
            orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5,
            font=dict(color='white', size=10)
        ),
        xaxis=dict(tickfont=dict(color='white', size=8), tickangle=-45, gridcolor='#222'),
        yaxis=dict(tickfont=dict(color='white', size=10), gridcolor='#222', zerolinecolor='#333'),
        height=390,
        bargap=0.2,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# FILA 2: TICKETS ZOHO DESK
# ══════════════════════════════════════════════════════════════
st.markdown("""
    <div style="background:#1a1a1a;border-radius:10px;padding:10px 18px;
                border:1px solid #2a2a2a;margin-bottom:12px;">
        <span style="color:white;font-size:13px;font-weight:700;letter-spacing:1px;">
            🎫 TICKETS DE SOPORTE ZOHO DESK
            <span style="font-weight:400;color:#888;font-size:11px;">
                &nbsp;(Resumen de Backlog)
            </span>
        </span>
    </div>
""", unsafe_allow_html=True)

col_sem, col_pie = st.columns([2, 1], gap="medium")

# ── SEMÁFORO ──────────────────────────────────────────────────
with col_sem:
    st.markdown(
        '<div style="text-align:center;color:white;font-size:13px;font-weight:600;'
        'margin-bottom:12px;">⚡ Semáforo de Criticidad</div>',
        unsafe_allow_html=True
    )
    t1, t2, t3 = st.columns(3, gap="small")

    with t1:
        st.markdown("""
            <div class="tkt-card red">
                <div class="tkt-lbl" style="color:#ff4b4b;">⚠️ VENCIDOS</div>
                <div class="tkt-sub">(Violación de SLA)</div>
                <div class="tkt-num" style="color:#ff4b4b;">7</div>
                <div class="tkt-foot" style="color:#ff4b4b;">Atención Urgente Requerida</div>
            </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
            <div class="tkt-card orng">
                <div class="tkt-lbl" style="color:#ff9f43;">⌛ SIN CIERRE</div>
                <div class="tkt-sub">(Pendientes de Flujo de Trabajo)</div>
                <div class="tkt-num" style="color:#ff9f43;">15</div>
                <div class="tkt-foot" style="color:#ff9f43;">Proceso Pendiente</div>
            </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
            <div class="tkt-card blue">
                <div class="tkt-lbl" style="color:#3b82f6;">✉️ ABIERTOS / NUEVOS</div>
                <div class="tkt-sub">(Sin Respuesta de Primera Atención)</div>
                <div class="tkt-num" style="color:#3b82f6;">18</div>
                <div class="tkt-foot" style="color:#3b82f6;">Carga de Trabajo Actual</div>
            </div>
        """, unsafe_allow_html=True)

# ── GRÁFICO DONA ──────────────────────────────────────────────
with col_pie:
    st.markdown('<div class="sec-hdr">📊 Distribución de Criticidad del Backlog</div>', unsafe_allow_html=True)

    df_pie = pd.DataFrame({
        'label': ['Vencidos', 'Pendientes Cierre', 'Abiertos/Nuevos'],
        'value': [7, 15, 18],
        'color': ['#ff4b4b', '#ff9f43', '#3b82f6']
    })
    fig_pie = px.pie(
        df_pie, values='value', names='label', hole=0.5,
        color_discrete_sequence=df_pie['color'].tolist()
    )
    fig_pie.update_layout(
        paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a',
        margin=dict(l=0, r=60, t=10, b=0),
        showlegend=True,
        legend=dict(
            orientation="v", yanchor="middle", y=0.5,
            xanchor="left", x=1.0, font=dict(color='white', size=11)
        ),
        height=260
    )
    fig_pie.update_traces(
        textposition='inside', textinfo='percent',
        textfont_size=13,
        marker=dict(line=dict(color='#1a1a1a', width=2))
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="footer-txt">
        Nota: Los tickets Vencidos representan una falla crítica en el SLA y deben ser escalados
        antes que la cola de 18 tickets abiertos (ITIL 4 best practice).<br>
        Generado por <strong>Techforce</strong> Data Analytics &nbsp;|&nbsp;
        1 DE ABRIL, 2026 &nbsp;|&nbsp; Versión: 2026.01.05
    </div>
""", unsafe_allow_html=True)