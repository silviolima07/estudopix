from PIL import Image
import numpy as np
import streamlit as st

import matplotlib.pyplot as plt

#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#import nltk

#from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

#pd.set_option('precision',2)

#import base64

import sys

#import glob

import time

import requests
from bs4 import BeautifulSoup


import json

from bokeh.plotting import figure

import altair as alt

st.set_option('deprecation.showPyplotGlobalUse', False)

df_ibge = pd.read_csv("base/df_cidades_ibge.csv", encoding='latin-1')   
#st.table(df_ibge)
df_ibge['uf'] = df_ibge['uf'].str.upper()
df_ibge['Estado'] = df_ibge['Estado'].str.upper()
    
pix = Image.open("img/pix.png")
#ibge = Image.open("img/ibge.png")

df_ibge['cidade_uf'] = df_ibge['Mun']+'-'+df_ibge['uf']
l_cidades = df_ibge.cidade_uf
l_cidades = sorted(l_cidades)

#url_pix_liq   colunas: Data	Quantidade	Total	Media
#url_intra_dia colunas: Horario	QuantidadeMedia	TotalMedio

# Pix liquidados atual
# Traz a data, quantidade, valor total e valor média das transações.
url_pix_liq = 'https://olinda.bcb.gov.br/olinda/servico/SPI/versao/v1/odata/PixLiquidadosAtual?$top=100&$format=json'

url_pix_liq_2023 = "https://olinda.bcb.gov.br/olinda/servico/SPI/versao/v1/odata/PixLiquidadosAtual?$top=365&$filter=Data%20ge%20%202023-01-01&$format=json"

# Pix liquidados intradia
# Traz por faixa de horario a quantidade média  e o valor médio das transações nos ultimos 30 dias.
url_intra_dia = 'https://olinda.bcb.gov.br/olinda/servico/SPI/versao/v1/odata/PixLiquidadosIntradia?$top=100&$format=json'



def extrair_dados(url):
  req = requests.get(url)
  info = req.json()
  #pprint.pformat(info)
  tabela = pd.DataFrame(info['value'])
  return tabela

def ajuste_vl(kpi):
  temp = str(kpi).split(',')
  inteiros = len(temp[0])
  decimais = len(temp[1])
  #st.write("inteiros: "+str(inteiros))
  #st.write("decimais: "+str(decimais))
  
  if decimais == 1:
    kpi = kpi+'0'
    #st.subheader(kpi)
  
  if inteiros == 15:
    kpi = 'R$ '+kpi[0:3]+' Bilhoes' 
    
  elif inteiros == 14:
    kpi = 'R$ '+kpi[0:3]+' Bilhoes' 
    
  elif inteiros == 13:
    kpi = 'R$ '+kpi[0:1]+'.'+kpi[2]+' Bilhoes'    

  elif inteiros == 12:
    kpi = 'R$ '+kpi[0:3]+' Bilhoes'  
    
  elif inteiros == 11:
    kpi = 'R$ '+kpi[0:2]+'.'+kpi[2:4]+' Bilhoes'
                
  elif inteiros == 10:
    kpi = 'R$ '+kpi[0:1]+'.'+kpi[1:3]+' Bilhoes'

  elif inteiros == 9:
    kpi = 'R$ '+kpi[0:3]+' Milhoes'
            
  elif inteiros == 8:
    kpi = 'R$ '+kpi[0:2]+'.'+kpi[2]+' Milhoes'      

  elif inteiros == 7:
      kpi = 'R$ '+kpi[0]+'.'+kpi[1]+' Milhoes'
 
  elif inteiros == 6:
      kpi = 'R$ '+kpi[0:3]+' Mil' 
                
  return kpi
  
def ajuste_qt(kpi):
  
  #st.subheader(kpi)
  inteiros = len(kpi)
  #
  
  #st.subheader("inteiros: "+str(kpi))
    
  if inteiros == 15:
    kpi = kpi[0:3]+' Bilhoes' 
    
  elif inteiros == 14:
    kpi = kpi[0:3]+' Bilhoes' 
    
  elif inteiros == 13:
    kpi = kpi[0:1]+'.'+kpi[2]+' Bilhoes'    

  elif inteiros == 12:
    kpi = kpi[0:3]+' Bilhoes'  
    
  elif inteiros == 11:
    kpi = kpi[0:2]+'.'+kpi[2:5]+' Bilhoes'
                
  elif inteiros == 10:
    kpi = kpi[0:1]+'.'+kpi[1:3]+' Bilhoes'

  elif inteiros == 9:
    kpi = kpi[0:3]+' Milhoes'
            
  elif inteiros == 8:
    kpi = kpi[0:2]+'.'+kpi[2]+' Milhoes'      

  elif inteiros == 7:
      kpi = kpi[0]+'.'+kpi[1:3]+' Milhoes'
 
  elif inteiros == 6:
      kpi = kpi[0:3]+' Mil' 
                
  return kpi  
    
dict_mes = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}  

dict_uf_estado = {'SP':'SÃO PAULO', 'RJ':'RIO DE JANEIRO', 'DF':'DISTRITO FEDERAL', 'BA':'BAHIA', 'CE':'CEARÁ', 'MG':'MINAS GERAIS', 'AM':'AMAZONAS', 'PR':'PARANÁ', 'MA':'MARANHÃO', 'AL':'ALAGOAS', 'RN':'RIO GRANDE DO NORTE', 'PB':'PARAÍBA', 'SE':'SERGIPE', 'SC': 'SANTA CATARINA', 'GO': 'GOIÁS', 'RO': 'RONDÔNIA', 'RR': 'RORAIMA', 'PA': 'PARÁ', 'MT': 'MATO GROSSO', 'MS': 'MATO GROSSO DO SUL', 'ES':'ESPIRITO SANTO', 'PI': 'PIAUÍ', 'RS': 'RIO GRANDE DO SUL', 'PE': 'PERNAMBUCO', 'AC': 'ACRE', 'AP': 'AMAPÁ', 'TO': 'TOCANTINS' }  

with open('style.css') as f:
              st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():

    """Pix App """

   
    #st.sidebar.image(logo_seriea,caption="", width=300)

    activities = ["Estudo", "Por Cidade","Transações Ao Longo do Dia", 
    "Transações em 2023","Sobre"]
     
    
    

    choice = st.sidebar.selectbox("MENU",activities)
    
    #df = pd.read_csv("CSV/dados_2012_2023.csv")
    
    #df_2023 = pd.read_csv("CSV/dados_2023.csv")

    # Definir a data da última atualização

    
    if choice == activities[0]: # Estudo
    
           
        html_page_activiy_0 = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:32px;font-weight:bold;color:white'>Estudo Pix nas Cidades</p>
    </div>
              """
        st.markdown(html_page_activiy_0, unsafe_allow_html=True)
        
        st.markdown("#### Análise de dados de transações feitas via Pix nas cidades do Brasil.")
        #st.markdown("#### Dados populacionais foram acrescentados aos dados do Pix, para #checar a existência de possíveis padrões comuns entre as cidades.")
        
        flag = False
        
        col1,col2, col3 = st.columns(3)
        col4,col5, col6 = st.columns(3)
        col7,col8, col9 = st.columns(3)
        
        with col1:
          st.subheader('Fonte: ')
        with col5:
          st.markdown('### API Pix')
          st.image(pix, width=220)
        #with col5:  
        #  st.image(ibge, width=200)
        
       
    elif choice == activities[1]:
        html_page_cidades = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:32px;font-weight:bold;color:white'>Por Cidade</p>
    </div>
              """
        st.markdown(html_page_cidades, unsafe_allow_html=True)
        
        buscar = False
        
        #l_cidades = ['Piripiri-PI', 'Santos-SP']  
        default_ix = l_cidades.index('São Paulo-SP')        
        choice_cidade = st.selectbox("Cidade",l_cidades, label_visibility="hidden", index=default_ix)
                
        cidade = choice_cidade
        
        
        
         #buscar = True
        
        choice = choice_cidade.split('-')
        cidade = choice[0]
        #estado = choice[1]
        
        #st.write(cidade)
        #st.write(estado)
        #st.write(dict_uf_estado.get(estado))
        estado = dict_uf_estado.get(choice[1])
        
        url_cidade = "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/TransacoesPixPorMunicipio(DataBase=@DataBase)?@DataBase='2023'&$top=100&$filter=Municipio%20eq%20"+"'"+cidade+"'"+"&$format=json"
        
        url_cidade_uf = "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/TransacoesPixPorMunicipio(DataBase=@DataBase)?@DataBase='2023'&$top=5571&$filter=Municipio%20eq%20"+"'"+cidade+"'"+"%20and%20Estado%20eq%20"+"'"+estado+"'"+"&$format=json"
        
        #st.write(url_cidade_uf)
        
        if st.button("Buscar"):        
          try:
            
            df = extrair_dados(url_cidade_uf)
            
            #st.write(url_cidade_uf)
          
            with st.spinner('Processando...dados do Pix..de..'+cidade.upper()):
            #st.write(df)
              time.sleep(5)
              df['AnoMes'] = pd.to_datetime(df['AnoMes'], format='%Y%m')
              df['Ano'] = df.AnoMes.dt.year
              df['Mes'] = df.AnoMes.dt.month
          
              lista_mes =[]
              for i in df.Mes:
                lista_mes.append(dict_mes.get(i).upper())
              df['Mes'] = lista_mes
              #df['Mes_Ano'] = str(df.Ano.astype('int')
              df['MesAno'] = df['AnoMes'].dt.strftime('%m/%Y') 
          
              colunas = ['MesAno','AnoMes','Ano','Mes','VL_PagadorPF', 'QT_PagadorPF', 'VL_RecebedorPF', 'QT_RecebedorPF','VL_PagadorPJ', 'QT_PagadorPJ', 'VL_RecebedorPJ', 'QT_RecebedorPJ']
              #st.write(df)
              temp = df[colunas].copy()
              mes = temp['Mes']
              #st.write(temp['AnoMes'])
              #st.write(temp['AnoMes'], index=False)
              #st.subheader(str(mes[0:]))
              #st.write(temp['AnoMes'])
              #col_ano, col_mes = st.columns(2)
              st.header("Periodo")
              last_years = sorted(list(set(temp.Ano)))
              last_2_years = last_years[-2:]
              #l_ano = list(set(temp.Ano))
              #item_ano = l_ano[0]
              #for item in l_ano[1:]:
              #col_ano.subheader(item)
              #st.write(item)
              item_ano = str(last_2_years[0])+'-'+str(last_2_years[1])
              st.subheader(item_ano)
              #st.table(temp)
              html_page_kpi = """
      <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:white'>Indicadores</p>
      </div>
              """
              st.markdown(html_page_kpi, unsafe_allow_html=True)
         
              col1,col2, col3, col4 = st.columns(4)
              col5,col6, col7, col8 = st.columns(4)
              col9,col10, col11, col12 = st.columns(4)
          
        
            #with col1:
            #  kpi = " R$ "+str(np.round(temp.VL_PagadorPF.sum(),2)).replace(".",',')
              #st.write("KPI--> "+str(kpi))
          
            #with open('style.css') as f:
            #  st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
          #with col1:
          #  kpi = " R$ "+str(np.round(temp.VL_PagadorPF.sum(),2)).replace(".",',')
            #st.write("KPI--> "+str(kpi))  
           
          #col1, col2, col3,col4 = st.columns(4)
          #kpi = " R$ #"+str(np.round(temp.VL_PagadorPF.sum(),2)).replace(".",',')
              temp_2_years = temp.loc[temp.Ano >=  last_2_years[0]]
              temp = temp_2_years
                
            
              kpi_vl_pg_pf = str(np.round(temp.VL_PagadorPF.sum(),2)).replace(".",',')
              kpi_qt_pg_pf = str(np.round(temp.QT_PagadorPF.sum(),2)).replace(".",',')
              kpi_vl_rc_pf = str(np.round(temp.VL_RecebedorPF.sum(),2)).replace(".",',')
              kpi_qt_rc_pf = str(np.round(temp.QT_RecebedorPF.sum(),2)).replace(".",',')
            
              kpi_vl_pg_pj = str(np.round(temp.VL_PagadorPJ.sum(),2)).replace(".",',')
              kpi_qt_pg_pj = str(np.round(temp.QT_PagadorPJ.sum(),2)).replace(".",',')
              kpi_vl_rc_pj = str(np.round(temp.VL_RecebedorPJ.sum(),2)).replace(".",',')
              kpi_qt_rc_pj = str(np.round(temp.QT_RecebedorPJ.sum(),2)).replace(".",',')
          
              #st.subheader(kpi_vl_pg_pf)
              #size = str(kpi_vl_pg_pf).split(',')
              #st.subheader("kpi_vl_pg_pf inteiros: "+str(len(size[0])))
              #st.subheader("kpi_vl_pg_pf decimais: "+str(len(size[1])))
          
            
            
              col1.markdown("##### VL_PagadorPF")            
              col1.metric("teste", ajuste_vl(kpi_vl_pg_pf), label_visibility="collapsed")
              col2.markdown("##### QT_PagadorPF")  
              col2.metric("teste", ajuste_qt(kpi_qt_pg_pf),label_visibility="collapsed")
              col3.markdown("##### VL_RecebedorPF")  
              col3.metric("teste", ajuste_vl(kpi_vl_rc_pf),label_visibility="collapsed")
              col4.markdown("##### QT_RecebedorPF")  
              col4.metric("teste", ajuste_qt(kpi_qt_rc_pf),label_visibility="collapsed")
          
              col5.markdown("##### VL_PagadorPJ")  
              col5.metric("",ajuste_vl(kpi_vl_pg_pj),label_visibility="collapsed")
              col6.markdown("##### QT_PagadorPJ")  
              col6.metric("", ajuste_qt(kpi_qt_pg_pj),label_visibility="collapsed")
              col7.markdown("##### VL_PagadorPJ")  
              col7.metric("", ajuste_vl(kpi_vl_rc_pj),label_visibility="collapsed")
              col8.markdown("##### QT_PagadorPJ")  
              col8.metric("", ajuste_qt(kpi_qt_rc_pj),label_visibility="collapsed")
          
            # col9.markdown("##### VL_PagadorPF(R$)")
            # col9.metric("teste",ajuste(kpi),label_visibility="collapsed")
            # col10.markdown("##### VL_PagadorPF(R$)")
            # col10.metric("teste", ajuste(kpi),label_visibility="collapsed")
            # col11.markdown("##### VL_PagadorPF(R$)")
            # col11.metric("teste", ajuste(kpi),label_visibility="collapsed")
            # col12.markdown("##### VL_PagadorPF(R$)")
            # col12.metric("teste", ajuste(kpi),label_visibility="collapsed")
          
          #with st.spinner('Processando...'):
            
            st.success('Concluido!')
          
          except:
            st.write("Cidade não tem dados cadastrados")
          

    elif choice == activities[2]:
        html_page_cidades = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:white'>Transações Ao Longo do Dia</p>
    </div>
              """
        st.markdown(html_page_cidades, unsafe_allow_html=True)
        
        st.markdown("##### Quantidades e valores médios por intervalo de trinta minutos, nos últimos 30 dias.")
        st.markdown("##### Valores representados em milhares de R$")

        try:
          #pd.options.display.float_format = '{:.2f}'.format
          # df = extrair_dados(url_intra_dia)
          # df = df.rename(columns={'Horario':'index'}).set_index('index')
          # st.markdown("#### Quantidade de Transações")
          st.markdown("##### Periodo: 24h")
          # st.line_chart(df['QuantidadeMedia'])
          
          
          
          df = extrair_dados(url_intra_dia)
          
          def plot_line(coluna):
            if coluna == 'QuantidadeMedia':
              title='Quantidade Média de Transações'
            elif coluna == 'TotalMedio':
              title='Valor Total Médio em Milhões de Reais'
              df[coluna] = df[coluna]/1000        
            st.subheader(title)
            #coluna = coluna
            line_chart = alt.Chart(df).mark_line().encode(
              alt.X('Horario', title='Hora'),
              alt.Y(coluna, title=coluna+'(M)')
             ).configure_axis(
             labelFontSize=20,
             titleFontSize=20
                )
            st.altair_chart((line_chart).interactive(), use_container_width=True)
          
          
          plot_line('QuantidadeMedia')
          
          plot_line('TotalMedio')
          
          #max_qt = df.Qua
          
                             
          
        except:
          st.write("Erro na execução da chamada da API")
          
    elif choice == activities[3]:
        html_page_pix_2023 = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:white'>Transações em 2023</p>
    </div>
              """
        st.markdown(html_page_pix_2023, unsafe_allow_html=True)
        
        

        try:
          #pd.options.display.float_format = '{:.2f}'.format
          # df = extrair_dados(url_intra_dia)
          # df = df.rename(columns={'Horario':'index'}).set_index('index')
          # st.markdown("#### Quantidade de Transações")
          #st.markdown("##### Periodo: 24h")
          # st.line_chart(df['QuantidadeMedia'])
          
          
          
          df = extrair_dados(url_pix_liq_2023)
          
          def plot_line(coluna):
            if coluna == 'Quantidade':
              title='Quantidade de Transações em Milhoes'
              label_y = "Qtd Transações"
              temp = df.copy()
              temp[coluna] = temp[coluna]
            elif coluna == 'Total':
              title='Valor Total em Bilhões de Reais'
              label_y = "Total Transações(R$)"
              temp = df.copy()
              temp[coluna] = temp[coluna]
            else:
              title='Valor Médio em Reais'
              label_y = "Media(R$)"
              temp = df.copy()
              temp[coluna] = temp[coluna]                 
            
            st.subheader(title)
            #coluna = coluna
            line_chart = alt.Chart(df).mark_line().encode(
              alt.X('Data', title='Data'),
              alt.Y(coluna, title=label_y)
             ).configure_axis(
             labelFontSize=20,
             titleFontSize=20
                )
            st.altair_chart((line_chart).interactive(), use_container_width=True)
          
          opcao = st.sidebar.radio(
    "Escolha o gráfico:",
    ["Quantidade de Transações", "Valor Total em Reais", "Valor Médio"])

          if opcao == 'Quantidade de Transações':
            
            plot_line('Quantidade')
            
            st.markdown("#### Obs:")# amplie o gráfico para ver melhor, no canto superior #direito.")
            st.markdown("##### amplie o gráfico para ver melhor, clique no canto superior direito.")
            
          elif opcao == "Valor Total em Reais":
            plot_line('Total')
            
            st.markdown("#### Obs:")# amplie o gráfico para ver melhor, no canto superior #direito.")
            st.markdown("##### amplie o gráfico para ver melhor, clique no canto superior direito.")
            
            st.markdown("### Records em 2023")       
        
            st.subheader('Maior Quantidade de Transações')
            temp = df.copy()
            temp['Total'] = temp['Total']*1000
            df_max_qtd = temp.loc[temp.Quantidade == temp.Quantidade.max()]
            df_max_total = temp.loc[temp.Total == temp.Total.max()]
          
            st.subheader(ajuste_qt(str(df_max_qtd.Quantidade.max()))+" no Dia: "+str(df_max_qtd.Data.max()))
          
            st.subheader('Maior Valor(R$)')

            st.subheader(ajuste_vl(str(df_max_total.Total.max()).replace('.',','))+" no Dia: "+str(df_max_total.Data.max()))
          else:
            plot_line('Media')
            
            st.markdown("#### Obs:")# amplie o gráfico para ver melhor, no canto superior #direito.")
            st.markdown("##### amplie o gráfico para ver melhor, clique no canto superior direito.")
          
          
          
        
          
          
          #st.subheader(df.Media.max())
          
                             
          
        except:
          st.write("Erro na execução da chamada da API") 
     
        
          
        
    
        
       
    elif choice == 'Sobre':
        html_page_about = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:left;font-size:32px;font-weight:bold;color:white'>Saiba mais...</p>
    </div>
              """
        st.markdown(html_page_about, unsafe_allow_html=True)
        
        st.subheader("Dicionário de dados:")
               
        st.markdown("##### VL_PagadorPF")
        st.markdown("##### -> Volume financeiro em R$ das transações cujo Pagador é uma pessoa física (PF)")
        
        st.markdown("##### QT_PagadorPF")
        st.markdown("##### -> Quantidade de transações cujo Pagador é uma pessoa física (PF)")
        
        st.markdown("##### VL_RecebedorPF")
        st.markdown("##### ->Volume financeiro em R$ das transações cujo Recebedor é uma pessoa física (PF)")
        
        st.markdown("##### QT_RecebedorPF")
        st.markdown("##### -> 	Quantidade de transações cujo Recebedor é uma pessoa física (PF)")
        
        #st.markdown("##### Transações Ao Longo do Dia")
    
        
        st.markdown("##### Dados coletados do Pix via api do Banco Central.")# e dados das #cidades disponíveis no IBGE.")
        
        st.markdown("##### Fonte dos dados: ")
        st.markdown("##### https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/aplicacao#!/recursos")
        st.markdown("##### https://olinda.bcb.gov.br/olinda/servico/SPI/versao/v1/aplicacao#!/recursos")
        
      
        st.subheader("Silvio Lima")
        
        st.markdown('#### https://www.linkedin.com/in/silviocesarlima/')
       
    
    
       

   
      
if __name__ == '__main__':
    main()




