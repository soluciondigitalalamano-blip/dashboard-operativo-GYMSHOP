import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. Configuración de la página (Modo oscuro y layout ancho)
st.set_page_config(layout="wide", page_title="Cuadro Técnicos Semanal")

# 2. Carga y Preprocesamiento de Datos
raw_data = {
    'Técnico': [
        'CONTRERAS CORZO JAVIER ALEXANDER', 'JESUS ARMANDO JOYA DIAZ', 'VARGAS RESTREPO ANDRES FELIPE',
        'ACOSTA MARTINEZ OSMAN OMAR', 'RONCANCIO BELTRAN WILSON EMEIRO', 'LOPEZ GIRALDO JAMIR',
        'GOMEZ CARDENAS MAURICIO', 'RODRIGUEZ CESAR AUGUSTO', 'CARDOZO CASTRO EDGAR GIOVANNY',
        'JIMENEZ VELOZA LUCINIO IVAN', 'JAVIER ESTIVEN MORA', 'VANEGAS YONI ALBEIRO',
        'ROMERO SERRANO LUIS MIGUEL', 'PAJARO ESCORCIA MARTIN', 'RIOS ARANGO ADRIAN ALONSO'
    ],
    'Visitas registradas': [5, 1, 2, 0, 0, 1, 2, 3, 4, 2, 1, 0, 2, 2, 1],
    'Agenda semana pasada': [6, 4, 2, 2, 5, 5, 6, 7, 3, 5, 6, 4, 4, 4, 2],
    '% de visitas vs agenda': [
        '83.3 %', '25.0 %', '100.0 %', '0.0 %', '0.0 %', '20.0 %', '33.3 %', '42.9 %',
        '133.3 %', '40.0 %', '16.7 %', '0.0 %', '50.0 %', '50.0 %', '50.0 %'
    ],
    'Gastos': [
        '590.650 COP', '0 COP', '86.900 COP', '0 COP', '0 COP', '30.000 COP', '36.400 COP',
        '0 COP', '51.000 COP', '45.000 COP', '37.100 COP', '0 COP', '0 COP', '0 COP', '18.000 COP'
    ],
    'Cantidad de ventas reportada': [4, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 1],
    'Servicios agendados esta semana': [2, 4, 4, 4, 1, 4, 3, 3, 1, 3, 1, 0, 0, 0, 0]
}

# Crear DataFrame
df = pd.DataFrame(raw_data)

# Preprocesar datos numéricos para cálculos
def clean_cop(str_val):
    if not isinstance(str_val, str): return str_val
    clean_val = str_val.replace('COP', '').replace('.', '').strip()
    return int(clean_val) if clean_val else 0

df['Gastos_num'] = df['Gastos'].apply(clean_cop)
df['% Cumplimiento_num'] = df['% de visitas vs agenda'].str.replace(' %', '').astype(float) / 100

# 3. Recalcular métricas principales
total_ventas = df['Cantidad de ventas reportada'].sum()
total_gastos = df['Gastos_num'].sum()
total_visitas = df['Visitas registradas'].sum()
total_agenda = df['Agenda semana pasada'].sum()
cumplimiento_promedio = (total_visitas / total_agenda) * 100 if total_agenda > 0 else 0

# 4. Definir CSS personalizado para estilos oscuros y bordes redondeados
custom_css = """
<style>
    body { background-color: #121212 !important; color: #f0f0f0 !important; font-family: sans-serif !important; }
    h1, h2, h3 { color: white !important; }
    .dashboard-panel { background-color: #1a1a1a; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .metric-card-container { display: flex; flex-direction: column; align-items: flex-start; color: #f0f0f0; }
    .metric-value { font-size: 36px; font-weight: bold; color: white; }
    .metric-label { font-size: 14px; color: #a0a0a0; margin-bottom: 10px; }
    .trend-positive { color: #50e3c2; font-size: 14px; }
    .ticket-card { background-color: #1a1a1a; border-radius: 10px; padding: 20px; margin: 10px; color: #f0f0f0; display: flex; flex-direction: column; align-items: center; text-align: center; }
    .ticket-card.red { border: 2px solid #ff4b4b; }
    .ticket-card.orange { border: 2px solid #ff9f43; }
    .ticket-card.blue { border: 2px solid #3b82f6; }
    .ticket-value { font-size: 64px; font-weight: bold; }
    .ticket-label { font-size: 14px; font-weight: bold; }
    .ticket-desc { font-size: 12px; color: #a0a0a0; }
    .dashboard-footer { color: #a0a0a0; font-size: 10px; padding: 10px; text-align: center; }
    div[data-testid="stVerticalBlock"] > div:has(div.metric-card-container) { padding: 0px !important; }
    div[data-testid="stContainer"] { background-color: transparent !important; }
    .ticket-banner { background-color: transparent !important; border-bottom: 1px solid #333; margin-bottom: 10px; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 5. Header (Branding, Título, Filtros)
with st.container():
    col1, col2, col3 = st.columns([1, 4, 2])
    with col1:
        st.markdown(
            '<div style="color: white; font-weight: bold; font-size: 24px;">GYM <span style="font-size: 10px; vertical-align: super; color: #ff4b4b;">Shop</span><sup>®</sup></div>'
            '<div style="color: #a0a0a0; font-size: 10px;">Bienestar, Salud & Felicidad</div>'
            '<div style="color: white; font-size: 10px; margin-top: 5px;">CON MÁS DE <br> <span style="font-size: 16px; font-weight: bold;">30 AÑOS</span> <br> TRAYECTORIA</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown('<h1 style="text-align: center;">CUADRO TÉCNICOS SEMANAL</h1>', unsafe_allow_html=True)
    with col3:
        st.markdown(
            '<div style="display: flex; align-items: center; justify-content: flex-end; color: #a0a0a0;">'
            '<div style="margin-right: 10px;">Techforce SOLUTIONS</div>'
            '<div style="margin-right: 20px;">1 DE ABRIL, 2026</div>'
            '</div>',
            unsafe_allow_html=True
        )
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.selectbox("Filtrar por Técnico", ["Todos"], index=0, key="tech_filter", label_visibility="collapsed")
        with f_col2:
            st.date_input("Rango de Fecha", label_visibility="collapsed")

# 6. Fila 1: Resumen Técnicos y Gráfico de Barras
col_left, col_right = st.columns([3, 2])

with col_left:
    with st.container():
        st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
        st.markdown('<h3>📈 RESUMEN TÉCNICOS</h3>', unsafe_allow_html=True)
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.markdown(
                f'<div class="metric-card-container"><div style="font-size: 48px; color: white; margin-bottom: 10px;">💳</div>'
                f'<div class="metric-label">TOTAL VENTAS REPORTADAS</div><div class="metric-value">{total_ventas}</div>'
                f'<div class="trend-positive">📈 +12% vs. mes anterior</div></div>', unsafe_allow_html=True
            )
        with kpi_col2:
            st.markdown(
                f'<div class="metric-card-container"><div style="font-size: 48px; color: white; margin-bottom: 10px;">💰</div>'
                f'<div class="metric-label">TOTAL GASTOS OPERATIVOS</div><div class="metric-value">COP {total_gastos:,.0f}</div>'
                f'<div class="trend-positive">📉 -5% vs. mes anterior</div></div>', unsafe_allow_html=True
            )
        with kpi_col3:
            st.markdown(
                f'<div class="metric-card-container"><div style="font-size: 48px; color: white; margin-bottom: 10px;">📊</div>'
                f'<div class="metric-label">% CUMPLIMIENTO PROMEDIO (Vs Agenda)</div><div class="metric-value">{cumplimiento_promedio:.1f}%</div>'
                f'<div class="trend-positive">📈 +3.1% vs. mes anterior</div></div>', unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # AQUÍ ESTÁ LA CORRECCIÓN DE LA TABLA
    with st.container():
        st.markdown('<div class="dashboard-panel" style="background-color: #1a1a1a;">', unsafe_allow_html=True)
        st.markdown('<h3>📊 DETALLE DE OPERACIÓN POR TÉCNICO</h3>', unsafe_allow_html=True)
        
        columnas_originales = [
            'Técnico', 'Visitas registradas', 'Agenda semana pasada', 
            '% de visitas vs agenda', 'Gastos', 'Cantidad de ventas reportada', 
            'Servicios agendados esta semana'
        ]
        df_display = df[columnas_originales].copy()
        df_display.columns = ['Técnico', 'Visitas', 'Agenda', '% Cumplimiento', 'Gastos', 'Ventas', 'Agendados S.F.']
        
        fig_table = go.Figure(data=[go.Table(
            header=dict(values=list(df_display.columns), fill_color='#1a1a1a', align='left', font=dict(color='white', size=12), line_color='#333'),
            cells=dict(values=[df_display[col] for col in df_display.columns], fill_color=['#1a1a1a', '#222'] * 15, align='left', font=dict(color='#f0f0f0', size=11), line_color='#333')
        )])
        fig_table.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a')
        st.plotly_chart(fig_table, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    with st.container():
        st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
        st.markdown('<h3>📊 COMPARATIVA: VISITAS REALES VS. AGENDADAS</h3>', unsafe_allow_html=True)
        
        df_chart = df.copy()
        def shorten_tech_name(full_name):
            parts = full_name.split()
            return f"{parts[0]} {parts[1][0]}." if len(parts) >= 2 else parts[0]
            
        df_chart['Técnico_Abrev'] = df_chart['Técnico'].apply(shorten_tech_name)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_chart['Técnico_Abrev'], y=df_chart['Visitas registradas'], name='Visitas Reales', marker_color='white', offsetgroup=0))
        fig_bar.add_trace(go.Bar(x=df_chart['Técnico_Abrev'], y=df_chart['Agenda semana pasada'], name='Agenda Planificada', marker_color='#a0a0a0', offsetgroup=1))
        
        fig_bar.update_layout(
            paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', margin=dict(l=10, r=10, t=30, b=60),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')),
            xaxis=dict(tickfont=dict(color='white', size=10), tickangle=-45, gridcolor='#333'),
            yaxis=dict(tickfont=dict(color='white'), gridcolor='#333', zerolinecolor='#333')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 7. Fila 2: Tickets de Soporte Zoho Desk
st.markdown('<div class="dashboard-panel ticket-banner"><h3>🎫 TICKETS DE SOPORTE ZOHO DESK (Resumen de Backlog)</h3></div>', unsafe_allow_html=True)

col_tickets_left, col_tickets_right = st.columns([2, 1])

with col_tickets_left:
    st.markdown('<div class="dashboard-panel" style="background-color: transparent; box-shadow: none;"><h3>⚡ Semáforo de Criticidad</h3>', unsafe_allow_html=True)
    t_col1, t_col2, t_col3 = st.columns(3)
    
    with t_col1:
        st.markdown('<div class="ticket-card red"><div class="ticket-label" style="color: #ff4b4b;">⚠️ VENCIDOS</div><div class="ticket-desc">(Violación de SLA)</div><div class="ticket-value" style="color: #ff4b4b;">7</div><div style="font-size: 10px; color: #ff4b4b;">Atención Urgente Requerida</div></div>', unsafe_allow_html=True)
    with t_col2:
        st.markdown('<div class="ticket-card orange"><div class="ticket-label" style="color: #ff9f43;">⌛ SIN CIERRE</div><div class="ticket-desc">(Pendientes de Flujo de Trabajo)</div><div class="ticket-value" style="color: #ff9f43;">15</div><div style="font-size: 10px; color: #ff9f43;">Proceso Pendiente</div></div>', unsafe_allow_html=True)
    with t_col3:
        st.markdown('<div class="ticket-card blue"><div class="ticket-label" style="color: #3b82f6;">✉️ ABIERTOS / NUEVOS</div><div class="ticket-desc">(Sin Respuesta de Primera Atención)</div><div class="ticket-value" style="color: #3b82f6;">18</div><div style="font-size: 10px; color: #3b82f6;">Carga de Trabajo Actual</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_tickets_right:
    with st.container():
        st.markdown('<div class="dashboard-panel" style="padding: 10px 20px;"><h3>📊 DISTRIBUCIÓN DE CRITICIDAD</h3>', unsafe_allow_html=True)
        
        df_pie = pd.DataFrame({'label': ['Vencidos', 'Pendientes Cierre', 'Abiertos/Nuevos'], 'value': [7, 15, 18], 'color': ['#ff4b4b', '#ff9f43', '#3b82f6']})
        fig_pie = px.pie(df_pie, values='value', names='label', hole=0.5, color_discrete_sequence=df_pie['color'])
        fig_pie.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', margin=dict(l=0, r=0, t=10, b=0), showlegend=True, legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.1, font=dict(color='white')))
        fig_pie.update_traces(textposition='inside', textinfo='percent', textfont_size=16, marker=dict(line=dict(color='#1a1a1a', width=2)))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 8. Footer
st.markdown('<div class="dashboard-footer">Nota: Los tickets Vencidos representan una falla crítica en el SLA y deben ser escalados antes que la cola de 18 tickets abiertos (ITIL 4 best practice). <br>Generado por Techforce Data Analytics <br>1 DE ABRIL, 2026 | Versión: 2026.01.05</div>', unsafe_allow_html=True)