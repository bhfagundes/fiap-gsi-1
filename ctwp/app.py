import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

class EnergyDashboard:
    def __init__(self):
        st.set_page_config(
            page_title="Sistema de Gestão Energética",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    def generate_mock_data(self):
        # Gerar dados simulados para teste
        dates = pd.date_range(start='2024-01-01', periods=24, freq='H')
        return pd.DataFrame({
            'timestamp': dates,
            'consumo': np.random.normal(2.5, 0.5, 24),
            'luminosidade': np.random.randint(0, 100, 24),
            'presenca': np.random.choice([0, 1], 24)
        })

    def render_dashboard(self):
        # Cabeçalho
        st.title("⚡ Sistema de Gestão Energética Residencial")
        
        # Dados simulados
        df = self.generate_mock_data()
        
        # Status do Sistema
        st.sidebar.header("Status do Sistema")
        system_status = st.sidebar.success("Sistema Online")
        
        # Controles
        st.sidebar.subheader("Controles")
        modo = st.sidebar.selectbox(
            "Modo de Operação",
            ["Automático", "Manual", "Economia"]
        )
        
        if modo == "Manual":
            st.sidebar.slider("Intensidade da Luz", 0, 100, 50)
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Consumo Atual",
                f"{df['consumo'].iloc[-1]:.2f} kWh",
                f"{(df['consumo'].iloc[-1] - df['consumo'].iloc[-2]):.2f} kWh"
            )
        with col2:
            st.metric(
                "Luminosidade",
                f"{df['luminosidade'].iloc[-1]}%",
                "Normal"
            )
        with col3:
            st.metric(
                "Presença",
                "Detectada" if df['presenca'].iloc[-1] else "Não Detectada"
            )
        with col4:
            st.metric(
                "Economia Hoje",
                "15%",
                "↑ 2%"
            )
        
        # Gráfico de consumo
        st.subheader("📊 Monitoramento em Tempo Real")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['consumo'],
            name='Consumo',
            line=dict(color='#2E86C1')
        ))
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Alertas e Recomendações
        st.subheader("📝 Alertas e Recomendações")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Alertas Ativos**\n- Consumo acima da média no quarto\n- Verificar sensor da área externa")
        with col2:
            st.success("**Economia Projetada**\n- Diária: R$ 3,50\n- Mensal: R$ 105,00")

if __name__ == "__main__":
    dashboard = EnergyDashboard()
    dashboard.render_dashboard() 