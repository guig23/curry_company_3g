# Bibliotecas - libraries
import streamlit as st 
import pandas as pd
import plotly.express as pl
from haversine import haversine 
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
import folium 
from streamlit_folium import folium_static
#Carregar o arquivo 
df1 = pd.read_pickle('dflimpo.pkl')
df = df1.copy()
#print(df.dtypes)
st.set_page_config( page_title='Visão Entregadores', page_icon='🏍️', layout='wide')
#Cor da Barra Lateral: Usa CSS dentro do markdown!
#Funções:
def delivery_by_density(df):
    df_aux = (df.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby(['Road_traffic_density'])
                                                                            .agg({'Delivery_person_Ratings': ['mean', 'std']}))
    df_aux.columns = ['Média', 'Desvio Padrão']
    df_aux = df_aux.reset_index()
    st.dataframe(df_aux)
    st.markdown('##### Avaliação Média por Clima')
    df_aux = (df.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions'])
                                                                            .agg({'Delivery_person_Ratings': ['mean', 'std']}))
    df_aux.columns = ['Média', 'Desvio Padrão']
    df_aux = df_aux.reset_index() 
    return df_aux

def ten_fastest_delivery(df):
    df2 = df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'], ascending = True).reset_index()
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian ', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ', :].head(10)
    #Concatenar os 3 dataframes auxiliares:
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3

def ten_lowest_delivery(df):
    df2 = df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).max().sort_values(['City', 'Time_taken(min)'], ascending = False).reset_index()
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian ' , :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ', :].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3
#----------------------------------
#Limpeza extra:
df['Time_taken(min)'] = df['Time_taken(min)'].astype(str).apply(lambda x: x.split('(min)')[1])
df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
#Sidebar - Barra Lateral:
st.markdown("""
<style>

/* fundo geral */
.stApp{
    background-color:#141414;
    color:white;
}

/* sidebar */
[data-testid="stSidebar"]{
    background-color:#000000;
}

/* linha divisória */
hr{
    border:1px solid #333333;
}

/* títulos */
h1,h2,h3{
    color:white;
}

/* slider linha cinza */
.stSlider > div > div > div{
    background-color:#333333;
}

/* slider parte selecionada */
.stSlider > div > div > div > div{
    background-color:#E50914;
}

/* bolinha slider */
.stSlider > div > div > div > div > div{
    background-color:#E50914;
    border:2px solid white;
}

/* DIMINUI ESPAÇAMENTO NA SIDEBAR */
[data-testid="stSidebar"] .block-container{
    padding-top:1rem;
    padding-bottom:0rem;
}

[data-testid="stSidebar"] .element-container{
    margin-bottom:5px;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3{
    margin-bottom:5px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
#image_path = r"C:\Users\Guilherme G\Desktop\reposs\curry_company\logo_curry.png"
image = Image.open('logo_curry.png')
st.sidebar.image(image)
st.sidebar.markdown("## CURRY COMPANY -  O Delivery mais rápido da cidade!")
st.sidebar.markdown("---")
st.sidebar.markdown("### Selecione uma data limite")

date_slider = st.sidebar.slider(
    "Até qual data?",
    value=datetime(2022,4,13),
    min_value=datetime(2022,2,11),
    max_value=datetime(2022,4,13),
    format="DD-MM-YYYY"
)

traffic_options = st.sidebar.multiselect(
    "### Quais as condições de trânsito?",
    ['Low ','Medium ','High ','Jam '],
    default=['Low '])

st.sidebar.markdown("Powered by **Guilherme G. Guimarães**")

#Criar uma cópia do df original para fazer os filtros:

#Filtro de datas:
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas, :]
#st.dataframe(df)

#Filtro dos tipos de tráfego:
linhas_trafego = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_trafego, :]
#st.dataframe(df)

#Layout - STREAMLIT
st.header("MARKETPLACE - VISÃO ENTREGADORES")

tab1, tab2, tab3 = st.tabs(['Visão Gerencial das Entregas', '-', '-'])
with tab1:
    with st.container():
        st.title('Métricas Gerais')
        col1, col2, col3, col4 = st.columns(4, gap = 'large')
        with col1:
            #st.subheader('Maior idade')
            maior_idade = df.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior Idade é:',maior_idade)
            
        with col2:
            #st.subheader('Menor idade')
            menor_idade = df.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade é:', menor_idade)
        with col3:
            melhor_veiculo = df.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição de Veículo é:', melhor_veiculo)
        with col4:
            pior_veiculo = df.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição de Veículo é:', pior_veiculo)
    with st.container():
        st.markdown("""---""")
        st.title('Questões Climáticas e de Trânsito')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliação Média por Entregador')
            df_aux = df.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_aux)
        with col2: 
            st.markdown('##### Avaliação Média por Trânsito')
            fig = delivery_by_density(df)
            st.dataframe(fig)
            
    with st.container():
        st.markdown("""---""")
        st.markdown("<h2 style='text-align: center;'>Velocidade dos Entregadores</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>Top 10 - Mais Rápidos</h3>", unsafe_allow_html=True)
            fig = ten_fastest_delivery(df)
            st.dataframe(fig)
        with col2: 
            st.markdown("<h3 style='text-align: center;'>Top 10 - Mais Lentos</h3>", unsafe_allow_html=True)
            fig = ten_lowest_delivery(df)
            st.dataframe(fig)

#1. A menor e maior idade dos entregadores.
#print(df['Delivery_person_Age'].max())
#print(df['Delivery_person_Age'].min())

#2. A pior e a melhor condição de veículos.
#print(df['Vehicle_condition'].min())
#print(df['Vehicle_condition'].max())

#3.A avaliação média por entregador
#df_aux = df.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
#print(df_aux)

#4. A avaliação média e o desvio padrão por tipo de tráfego
#df_aux = (df.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby(['Road_traffic_density'])
#                                                                         .agg({'Delivery_person_Ratings': ['mean', 'std']}))
#df_aux.columns = ['Média', 'Desvio Padrão']
#df_aux = df_aux.reset_index()
#print(df_aux)

# 5. A avaliação média e o desvio padrão por condições climáticas.
#df_aux = (df.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions'])
#                                                                     .agg({'Delivery_person_Ratings': ['mean', 'std']}))
#df_aux.columns = ['Média', 'Desvio Padrão']
#df_aux = df_aux.reset_index() 
#print(df_aux)

#6. Os 10 entregadores mais rápidos por cidade.
#df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
#df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
#df2 = df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'], ascending = True).reset_index()
#df_aux01 = df2.loc[df2['City'] == 'Metropolitian ', :].head(10)
#df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
#df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ', :].head(10)
#Concatenar os 3 dataframes auxiliares:
#df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
#print(df3)

#7. Os 10 entregadores mais lentos por cidade.
#df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
#df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
#df2 = (df.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID'])
#                                                            .max()
#                                                            .sort_values(['City', 'Time_taken(min)'], ascending = False)
#                                                            .reset_index())
#df_aux01 = df2.loc[df2['City'] == 'Metropolitian ' , :].head(10)
#df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
#df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ', :].head(10)
#df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
#print(df3)