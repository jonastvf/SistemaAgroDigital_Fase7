#dashboard_main.py

import math as mt
import os
import csv
import sys
import shutil
import streamlit as st
import serial
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tensorflow as tf
import torch
import cv2
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from IPython.display import Image, display
from PIL import Image
#from models.models import SensorMPX
#from models.models import Base, SensorMPX, UnidadeMedida, AreaCapturada
from datetime import datetime

# Importa as funções da lógica das fases
# Crie estes arquivos nas respectivas pastas!
# from fase_1_dados import analise_insumos
# from fase_3_iot import controle_sensores
# from fase_6_visao import analise_yolo
# from fase_7_alerta import sns_publisher


# Entrada Central

try:
    from config import database_connection
    from config import config_aws 
    # Adicione aqui outros módulos de configuração, como o de credenciais AWS
except ImportError:
    st.error("Erro: Não foi possível importar os módulos de configuração. Verifique a pasta 'config'.")
    sys.exit()

# Função principal da Dashboard
def main():
    st.set_page_config(
        page_title="Sistema de Gestão Agronegócio - Fase 7",
        layout="wide"
    )

    st.title("🚜 Consolidação - Sistema de Gestão Agronegócio")

    # Verifica a conexão com o banco de dados logo no início
    if database.check_connection():
        st.sidebar.success("✅ Conexão DB (Fase 2) OK!")
    else:
        st.sidebar.error("❌ Erro de Conexão com o Banco de Dados (Fase 2)!")
    
    # Verifica status AWS (apenas exibe as credenciais lidas para verificação)
    if config_aws.AWS_ACCESS_KEY_ID != "SEU_ACCESS_KEY_AQUI":
        st.sidebar.info(f"☁️ Configuração AWS OK! Tópico: {config_aws.SNS_TOPIC_ARN.split(':')[-1]}")
    else:
        st.sidebar.warning("☁️ Configuração AWS PENDENTE! Alertas não funcionarão.")


# Abas de navegação entre os modulos
    tab_home, tab_f1, tab_f3, tab_f6, tab_alerta = st.tabs([
        "🏠 Visão Geral", 
        "📈 Insumos e Met. (F1)", 
        "💧 IoT e Irrigação (F3)", 
        "👁️ Visão Comp. (F6)",
        "☁️ Serviço de Alerta AWS (F7)"
    ])

    with tab_home:
        st.header("Status Geral do Sistema")
        st.write("Bem-vindo ao sistema consolidado. Utilize as abas acima para acessar as funcionalidades.")
        
        # Exibe um resumo dos dados do DB (Fase 2)
        st.subheader("Últimos Registros de Sensores (DB)")
        # ⚠️ Mude a query para refletir uma tabela real do seu DB
        df_sensores = database.fetch_data("SELECT * FROM dados_sensores LIMIT 5") 
        if not df_sensores.empty:
             st.dataframe(df_sensores, hide_index=True)
        else:
             st.info("Nenhum dado de sensor encontrado. Verifique a tabela no DB.")

    with tab_f1:
        st.header("Análise de Insumos e Dados Meteorológicos (Fase 1)")
        
        if st.button("Executar Cálculos e Análise Meteo (Fase 1)"):
            st.warning("Implemente a função de chamada da Fase 1 aqui!")
            # 💡 Exemplo de como chamar:
            # resultado = analise_insumos.executar_analise(database.get_connection())
            # st.success(resultado)

        
    with tab_f3:
        st.header("Controle de Sensores e Irrigação (Fase 3)")
        
        if st.button("Simular Leitura de Sensores e Lógica de Irrigação (Fase 3)"):
            st.warning("Implemente a função de chamada da Fase 3 aqui!")
            # 💡 Exemplo de como chamar:
            # resultado = controle_sensores.executar_logica(database.get_connection())
            # st.success(resultado)


    with tab_f6:
        st.header("Monitoramento Visual (Visão Computacional - Fase 6)")
        
        # Elemento para carregar a imagem para o YOLO
        uploaded_file = st.file_uploader("Selecione uma Imagem para Análise YOLO", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Imagem Carregada.", use_column_width=True)
            
            if st.button("Executar Detecção de Pragas (Fase 6)"):
                st.warning("Implemente a função de chamada da Fase 6 aqui!")
                # 💡 Exemplo de como chamar:
                # resultado_detecao = analise_yolo.detectar_praga(uploaded_file)
                # st.success(resultado_detecao)


    with tab_alerta:
        st.header("Configuração e Teste de Alerta AWS/SNS")
        
        st.subheader("1. Teste de Publicação de Alerta")
        
        alerta_titulo = st.text_input("Assunto do Alerta (E-mail)", "ALERTA CRÍTICO DE TESTE - Falha no Sistema")
        alerta_mensagem = st.text_area("Mensagem Completa (Corpo do Email/SMS)", 
                                       "Umidade do solo abaixo do limite de segurança. Ação: Verificar a bomba da Zona 2 imediatamente.")
        
        if st.button("Disparar Alerta de TESTE para Assinantes (Fase 7)", type="primary"):
            
            with st.spinner('Enviando alerta via AWS SNS...'):
                sucesso = sns_publisher.publicar_alerta(alerta_titulo, alerta_mensagem)
                
                if sucesso:
                    st.success("✅ Alerta de teste enviado com sucesso! Verifique a caixa de entrada dos emails/SMS cadastrados.")
                else:
                    st.error("❌ Falha ao enviar alerta. Verifique as credenciais AWS e o ARN do Tópico SNS no console/logs.")

        st.subheader("2. Monitoramento Automático (Integração Lógica)")
        st.info("Aqui, o sistema monitoraria os dados (Fase 3 ou Fase 6) e chamaria a função `publicar_alerta` automaticamente, se necessário.")
        
# Inicializa a aplicação Streamlit
if __name__ == "__main__":
    main()
