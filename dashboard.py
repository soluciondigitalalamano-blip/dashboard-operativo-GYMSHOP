import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="Dashboard Operativo y Soporte")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #1E3A8A; text-align: left; margin-bottom: 5px; }
    .section-header { 
        background-color: #F8FAFC; 
        padding: 10px; 
        border-left: 5px solid #1E3A8A; 
        font-weight: bold; 
        color: #1E3A8A; 
        margin-top: 30px; 
        margin-bottom: 15px; 
    }
    .kpi-rojo {
        background-color: #FEE2E2; 
        border: 1px solid #EF4444; 
        padding: 15px; 
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# SECCIÓN 1: RESUMEN TÉCNICOS
# ==========================================
st.markdown('<p class="main-title">📊 Resumen Técnicos</p>', unsafe_allow_html=True)

# 1. Carga de TODOS los datos de la imagen original
@st.cache_data
def load_data():
    data = {
        'Técnico': [
            'CONTRERAS CORZO JAVIER ALEXANDER', 'JESUS ARMANDO JOYA DIAZ', 'VARGAS RESTREPO ANDRES FELIPE', 
            'ACOSTA MARTINEZ OSMAN OMAR', 'RONCANCIO BELTRAN WILSON EMEIRO', 'LOPEZ GIRALDO JAMIR', 
            'GOMEZ CARDENAS MAURICIO', 'RODRIGUEZ CESAR AUGUSTO', 'CARDOZO CASTRO EDGAR GIOVANNY', 
            'JIMENEZ VELOZA LUCINIO IVAN', 'JAVIER ESTIVEN MORA', 'VANEGAS YONI ALBEIRO', 
            'ROMERO SERRANO LUIS MIGUEL', 'PAJARO ESCORCIA MARTIN', 'RIOS ARANGO ADRIAN ALONSO'
        ],
        'Visitas Registradas': [5, 1, 2, 0, 0, 1, 2, 3, 4, 2, 1, 0, 2, 2, 1],
        'Agenda Semana Pasada': [6, 4, 2, 2, 5, 5, 6, 7, 3, 5, 6, 4, 4, 4, 2],
        '% Visitas vs Agenda': [83.3, 25.0, 100.0, 0.0, 0.0, 20.0, 33.3, 42.9, 133.3, 40.0, 16.7, 0.0, 50.0, 50.0, 50.0],
        'Gastos (COP)': [590650, 0, 86900, 0, 0, 30000, 36400, 0, 51000, 45000, 37100, 0, 0, 0, 18000],
        'Ventas Reportadas': [4, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 1],
        'Servicios Agendados Esta Sem': [2, 4, 4, 4, 1, 4, 3, 3, 1, 3, 1, 0, 0, 0, 0] # Columna recuperada
    }
    return pd.DataFrame(data)

df = load_data()

# 2. Filtros en la barra lateral
st.sidebar.header("Filtros de Análisis")
selected_tecnicos = st.sidebar.multiselect(
    "Filtrar por Técnico:",
    options=sorted(df['Técnico'].unique()),
    default=sorted(df['Técnico'].unique())
)

df_filtered = df[df['Técnico'].isin(selected_tecnicos)]

# 3. KPIs de Técnicos
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Ventas Reportadas", f"{df_filtered['Ventas Reportadas'].sum()} u.")
with col2:
    gastos_totales = df_filtered['Gastos (COP)'].sum()
    st.metric("Total Gastos", f"${gastos_totales:,.0f} COP".replace(",", "."))
with col3:
    v_totales = df_filtered['Visitas Registradas'].sum()
    a_totales = df_filtered['Agenda Semana Pasada'].sum()
    cumplimiento = (v_totales / a_totales * 100) if a_totales > 0 else 0
    st.metric("% Cumplimiento Promedio", f"{cumplimiento:.1f}%")

# 4. Gráfico y Tabla
col_graf, col_tabla = st.columns([1.5, 2]) # Dividimos la pantalla para mejor uso del espacio

with col_graf:
    st.markdown("**Comparativa: Visitas vs Agenda**")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_filtered['Técnico'], y=df_filtered['Visitas Registradas'], name='Visitas Registradas', marker_color='#1E3A8A'))
    fig_bar.add_trace(go.Bar(x=df_filtered['Técnico'], y=df_filtered['Agenda Semana Pasada'], name='Agenda Planificada', marker_color='#94A3B8'))
    fig_bar.update_layout(barmode='group', height=350, margin=dict(t=10, b=10, l=10, r=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_tabla:
    st.markdown("**Detalle Operativo**")
    # Formatear gastos para la vista
    df_display = df_filtered.copy()
    df_display['Gastos (COP)'] = df_display['Gastos (COP)'].apply(lambda x: f"${x:,.0f}".replace(",", "."))
    st.dataframe(df_display, use_container_width=True, hide_index=True, height=350)


# ==========================================
# SECCIÓN 2: TICKETS ZOHO DESK
# ==========================================
st.markdown('<div class="section-header">🎫 Tickets de Soporte Zoho Desk</div>', unsafe_allow_html=True)

col_t1, col_t2, col_t3, col_t4 = st.columns([1, 1, 1, 1.5])

with col_t1:
    st.metric(label="Nuevos / Abiertos", value="18", delta="Sin Respuesta", delta_color="off")
    st.caption("Requieren primera atención.")

with col_t2:
    # KPI Crítico
    st.markdown('<div class="kpi-rojo">'
                '<h4 style="color: #B91C1C; margin:0;">⚠️ Vencidos (SLA)</h4>'
                '<h2 style="color: #B91C1C; margin:0; font-size: 36px;">7</h2>'
                '</div>', unsafe_allow_html=True)

with col_t3:
    st.metric(label="Pendientes Cierre", value="15", delta="Sin fecha entrega", delta_color="off")
    st.caption("En proceso pero sin cerrar.")

with col_t4:
    # Gráfico de Dona
    labels = ['Vencidos (SLA)', 'Abiertos (Sin Resp.)', 'Pendientes Cierre']
    values = [7, 18, 15]
    colors = ['#EF4444', '#3B82F6', '#F59E0B']
    
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=colors)])
    fig_pie.update_layout(
        height=200, 
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(orientation="v", y=0.5, x=1.1)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.info("**Prioridad Operativa:** Los 7 tickets vencidos representan un incumplimiento de SLA y deben ser escalados y atendidos con urgencia antes de procesar la cola de 18 tickets abiertos.")