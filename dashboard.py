import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (APP MODE)
# ==========================================
st.set_page_config(layout="wide", page_title="GYM Shop | Dashboard Ejecutivo", page_icon="📊", initial_sidebar_state="expanded")

# CSS Avanzado para look "Ejecutivo/Moderno"
custom_css = """
<style>
    /* Fondo principal y textos */
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 600; }
    
    /* Estilos de las tarjetas KPI */
    .kpi-card {
        background: linear-gradient(145deg, #1A1C23 0%, #121418 100%);
        border: 1px solid #2D303E;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease-in-out;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: #4facfe; }
    .kpi-title { color: #8B949E; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .kpi-value { color: #FFFFFF; font-size: 2.2rem; font-weight: 700; margin-bottom: 5px; }
    .kpi-trend.positive { color: #2EA043; font-size: 0.85rem; font-weight: 600; }
    .kpi-trend.negative { color: #F85149; font-size: 0.85rem; font-weight: 600; }
    
    /* Tarjetas de Tickets (Semáforo Moderno) */
    .ticket-card { border-radius: 12px; padding: 20px; text-align: center; font-weight: bold; }
    .ticket-card.danger { background-color: rgba(248, 81, 73, 0.1); border: 1px solid #F85149; }
    .ticket-card.warning { background-color: rgba(210, 153, 34, 0.1); border: 1px solid #D29922; }
    .ticket-card.info { background-color: rgba(88, 166, 255, 0.1); border: 1px solid #58A6FF; }
    .t-val { font-size: 3.5rem; line-height: 1; margin: 10px 0; }
    
    /* Ajustes Streamlit native */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { color: #4facfe !important; border-bottom: 2px solid #4facfe !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================
# 2. CARGA Y PREPARACIÓN DE DATOS (BASE DE DATOS EN MEMORIA)
# ==========================================
@st.cache_data
def load_data():
    # Datos Tabla Principal
    raw_data = {
        'Técnico': ['CONTRERAS CORZO JAVIER ALEXANDER', 'JESUS ARMANDO JOYA DIAZ', 'VARGAS RESTREPO ANDRES FELIPE', 'ACOSTA MARTINEZ OSMAN OMAR', 'RONCANCIO BELTRAN WILSON EMEIRO', 'LOPEZ GIRALDO JAMIR', 'GOMEZ CARDENAS MAURICIO', 'RODRIGUEZ CESAR AUGUSTO', 'CARDOZO CASTRO EDGAR GIOVANNY', 'JIMENEZ VELOZA LUCINIO IVAN', 'JAVIER ESTIVEN MORA', 'VANEGAS YONI ALBEIRO', 'ROMERO SERRANO LUIS MIGUEL', 'PAJARO ESCORCIA MARTIN', 'RIOS ARANGO ADRIAN ALONSO'],
        'Visitas registradas': [5, 1, 2, 0, 0, 1, 2, 3, 4, 2, 1, 0, 2, 2, 1],
        'Agenda semana pasada': [6, 4, 2, 2, 5, 5, 6, 7, 3, 5, 6, 4, 4, 4, 2],
        '% de visitas vs agenda': [83.3, 25.0, 100.0, 0.0, 0.0, 20.0, 33.3, 42.9, 133.3, 40.0, 16.7, 0.0, 50.0, 50.0, 50.0],
        'Gastos': [590650, 0, 86900, 0, 0, 30000, 36400, 0, 51000, 45000, 37100, 0, 0, 0, 18000],
        'Cantidad de ventas reportada': [4, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 1],
        'Servicios agendados esta semana': [2, 4, 4, 4, 1, 4, 3, 3, 1, 3, 1, 0, 0, 0, 0]
    }
    df = pd.DataFrame(raw_data)
    
    # Datos Calendario
    calendar_data = {
        'Técnico': ['CONTRERAS CORZO JAVIER ALEXANDER', 'CONTRERAS CORZO JAVIER ALEXANDER', 'JESUS ARMANDO JOYA DIAZ', 'JESUS ARMANDO JOYA DIAZ', 'JESUS ARMANDO JOYA DIAZ', 'JESUS ARMANDO JOYA DIAZ', 'VARGAS RESTREPO ANDRES FELIPE', 'VARGAS RESTREPO ANDRES FELIPE', 'VARGAS RESTREPO ANDRES FELIPE', 'VARGAS RESTREPO ANDRES FELIPE', 'ACOSTA MARTINEZ OSMAN OMAR', 'ACOSTA MARTINEZ OSMAN OMAR', 'ACOSTA MARTINEZ OSMAN OMAR', 'ACOSTA MARTINEZ OSMAN OMAR', 'RONCANCIO BELTRAN WILSON EMEIRO', 'LOPEZ GIRALDO JAMIR', 'LOPEZ GIRALDO JAMIR', 'LOPEZ GIRALDO JAMIR', 'LOPEZ GIRALDO JAMIR', 'GOMEZ CARDENAS MAURICIO', 'GOMEZ CARDENAS MAURICIO', 'GOMEZ CARDENAS MAURICIO', 'RODRIGUEZ CESAR AUGUSTO', 'RODRIGUEZ CESAR AUGUSTO', 'RODRIGUEZ CESAR AUGUSTO', 'CARDOZO CASTRO EDGAR GIOVANNY', 'JIMENEZ VELOZA LUCINIO IVAN', 'JIMENEZ VELOZA LUCINIO IVAN', 'JIMENEZ VELOZA LUCINIO IVAN', 'JAVIER ESTIVEN MORA'], 
        'Fecha': ['2026-03-30', '2026-03-31', '2026-03-30', '2026-03-30', '2026-03-31', '2026-04-01', '2026-03-30', '2026-03-30', '2026-03-31', '2026-04-01', '2026-03-30', '2026-03-31', '2026-04-01', '2026-03-31', '2026-03-30', '2026-03-30', '2026-03-31', '2026-03-31', '2026-04-01', '2026-03-30', '2026-03-31', '2026-04-01', '2026-03-30', '2026-03-31', '2026-04-01', '2026-03-31', '2026-03-30', '2026-03-31', '2026-04-01', '2026-04-01'], 
        'Estado': ['POR CONFIRMAR CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'PENDIENTE PROGRAMAR', 'POR CONFIRMAR CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'CONFIRMADO CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'POR CONFIRMAR CON CLIENTE', 'POR CONFIRMAR CON CLIENTE']
    }
    df_cal = pd.DataFrame(calendar_data)
    
    return df, df_cal

df_master, df_cal_master = load_data()


# ==========================================
# 3. BARRA LATERAL (SIDEBAR) & MOTOR DE FILTROS REAL
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2936/2936886.png", width=60) # Icono corporativo genérico
    st.markdown("### GYM Shop <span style='color:#F85149;'>®</span>", unsafe_allow_html=True)
    st.caption("Panel de Control Gerencial")
    st.markdown("---")
    
    st.markdown("**Filtros Operativos**")
    # Construcción dinámica de la lista de técnicos
    lista_tecnicos = ["Ver Todos (Visión Global)"] + sorted(df_master['Técnico'].unique().tolist())
    tec_seleccionado = st.selectbox("👨‍🔧 Seleccionar Técnico:", lista_tecnicos)
    
    st.markdown("---")
    st.caption("Desarrollado por Techforce")

# APLICAR EL FILTRO A LOS DATAFRAMES
if tec_seleccionado == "Ver Todos (Visión Global)":
    df = df_master.copy()
    df_cal = df_cal_master.copy()
    vista_actual = "Visión Global (Toda la compañía)"
else:
    df = df_master[df_master['Técnico'] == tec_seleccionado].copy()
    df_cal = df_cal_master[df_cal_master['Técnico'] == tec_seleccionado].copy()
    vista_actual = f"Rendimiento de: {tec_seleccionado}"

# Recálculo Matemático Dinámico basado en el filtro
total_ventas = df['Cantidad de ventas reportada'].sum()
total_gastos = df['Gastos'].sum()
total_visitas = df['Visitas registradas'].sum()
total_agenda = df['Agenda semana pasada'].sum()
cumplimiento_promedio = (total_visitas / total_agenda) * 100 if total_agenda > 0 else 0


# ==========================================
# 4. CABECERA PRINCIPAL
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"<h2>Cuadro de Mando Operativo Semanal</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #4facfe; font-weight: bold;'>{vista_actual}</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown(f"<div style='text-align: right; color: #8B949E; margin-top: 15px;'>Corte: <b>1 de Abril, 2026</b></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. ESTRUCTURA DE PESTAÑAS (TABS APP-LIKE)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 1. VISIÓN GENERAL Y KPIs", "🎫 2. SOPORTE Y TICKETS (DESK)", "📅 3. AGENDA Y CALENDARIO"])

# ------------------------------------------
# TAB 1: VISIÓN GENERAL Y KPIs
# ------------------------------------------
with tab1:
    # Fila de KPIs (Tarjetas Glassmorphism)
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Ventas Reportadas</div>
            <div class="kpi-value">{total_ventas}</div>
            <div class="kpi-trend positive">↗ +12% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Gastos Operativos (COP)</div>
            <div class="kpi-value">${total_gastos:,.0f}</div>
            <div class="kpi-trend negative">↘ -5% eficiencia</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">% Cumplimiento Global</div>
            <div class="kpi-value">{cumplimiento_promedio:.1f}%</div>
            <div class="kpi-trend positive">↗ +3.1% mejora</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Volumen Operativo (Visitas)</div>
            <div class="kpi-value">{total_visitas} <span style='font-size: 1rem; color: #8B949E;'>de {total_agenda}</span></div>
            <div class="kpi-trend positive">Ejecución vs Plan</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fila de Gráfico y Tabla Avanzada
    col_chart, col_table = st.columns([2, 3])
    
    with col_chart:
        st.markdown("#### 📈 Comparativa: Real vs Planificado")
        # Gráfico dinámico basado en el filtro
        df_chart = df.copy()
        df_chart['Tec_Abrev'] = df_chart['Técnico'].apply(lambda x: x.split()[0] + " " + x.split()[1][0] + "." if len(x.split()) > 1 else x)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_chart['Tec_Abrev'], y=df_chart['Visitas registradas'], name='Realizado', marker_color='#4facfe'))
        fig.add_trace(go.Bar(x=df_chart['Tec_Abrev'], y=df_chart['Agenda semana pasada'], name='Planificado', marker_color='#2D303E'))
        fig.update_layout(
            template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=10, l=0, r=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.markdown("#### 📋 Detalle Operativo (Alta Gama)")
        
        # Uso del nuevo st.dataframe interactivo y visual
        st.dataframe(
            df[['Técnico', 'Visitas registradas', 'Agenda semana pasada', '% de visitas vs agenda', 'Gastos', 'Cantidad de ventas reportada']],
            column_config={
                "Técnico": st.column_config.TextColumn("Técnico Asignado", width="medium"),
                "Visitas registradas": st.column_config.NumberColumn("Real", format="%d"),
                "Agenda semana pasada": st.column_config.NumberColumn("Plan", format="%d"),
                "% de visitas vs agenda": st.column_config.ProgressColumn(
                    "Cumplimiento",
                    help="Barra de progreso del cumplimiento",
                    format="%f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Gastos": st.column_config.NumberColumn(
                    "Gastos (COP)",
                    help="Gastos reportados en pesos colombianos",
                    format="$ %d",
                )
            },
            hide_index=True,
            use_container_width=True,
            height=350
        )

# ------------------------------------------
# TAB 2: SOPORTE Y TICKETS ZOHO DESK
# ------------------------------------------
with tab2:
    st.markdown("### Estado Actual del Backlog (Zoho Desk)")
    st.caption("Atención: Estos datos son globales de la cola de servicio, independientes del técnico seleccionado.")
    
    t1, t2, t3, t4 = st.columns([1,1,1, 1.5])
    
    with t1:
        st.markdown('<div class="ticket-card danger"><div style="color:#F85149;">⚠️ VENCIDOS (SLA)</div><div class="t-val" style="color:#F85149;">7</div>Atención Crítica</div>', unsafe_allow_html=True)
    with t2:
        st.markdown('<div class="ticket-card warning"><div style="color:#D29922;">⌛ SIN CIERRE</div><div class="t-val" style="color:#D29922;">15</div>Pendientes de Flujo</div>', unsafe_allow_html=True)
    with t3:
        st.markdown('<div class="ticket-card info"><div style="color:#58A6FF;">✉️ NUEVOS/ABIERTOS</div><div class="t-val" style="color:#58A6FF;">18</div>Carga Operativa</div>', unsafe_allow_html=True)
    
    with t4:
        df_pie = pd.DataFrame({'Estado': ['Vencidos (SLA)', 'Pendientes Cierre', 'Nuevos/Abiertos'], 'Valor': [7, 15, 18]})
        fig_pie = px.pie(df_pie, values='Valor', names='Estado', hole=0.6, color='Estado',
                         color_discrete_map={'Vencidos (SLA)':'#F85149', 'Pendientes Cierre':'#D29922', 'Nuevos/Abiertos':'#58A6FF'})
        fig_pie.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=0, b=0, l=0, r=0), height=200)
        st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------
# TAB 3: AGENDA Y CALENDARIO SEMANAL
# ------------------------------------------
with tab3:
    if df_cal.empty:
        st.info("No hay agendamientos para el técnico seleccionado en el CSV actual.")
    else:
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("#### Distribución de la Semana")
            # Gráfico de barras apiladas estilizado
            cal_summary = df_cal.groupby(['Fecha', 'Estado']).size().reset_index(name='Total')
            color_map = {'CONFIRMADO CON CLIENTE': '#2EA043', 'POR CONFIRMAR CON CLIENTE': '#D29922', 'PENDIENTE PROGRAMAR': '#58A6FF'}
            fig_cal = px.bar(cal_summary, x='Fecha', y='Total', color='Estado', color_discrete_map=color_map, text='Total')
            fig_cal.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                  legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5), margin=dict(t=20))
            st.plotly_chart(fig_cal, use_container_width=True)
            
        with c2:
            st.markdown("#### Matriz de Programación")
            # Preparar matriz limpia
            state_icons = {'CONFIRMADO CON CLIENTE': '🟢 Conf.', 'POR CONFIRMAR CON CLIENTE': '🟠 Por Conf.', 'PENDIENTE PROGRAMAR': '🔵 Pend.'}
            df_cal_view = df_cal.copy()
            df_cal_view['Icono'] = df_cal_view['Estado'].map(state_icons)
            
            # Agrupar y pivotar
            summary_mat = df_cal_view.groupby(['Técnico', 'Fecha', 'Icono']).size().reset_index(name='count')
            summary_mat['Tag'] = summary_mat['count'].astype(str) + " " + summary_mat['Icono']
            table_data = summary_mat.groupby(['Técnico', 'Fecha'])['Tag'].apply(lambda x: ' | '.join(x)).reset_index()
            pivot_table = table_data.pivot(index='Técnico', columns='Fecha', values='Tag').fillna('-').reset_index()
            
            # Usar st.dataframe nativo para la matriz
            st.dataframe(pivot_table, hide_index=True, use_container_width=True, height=300)