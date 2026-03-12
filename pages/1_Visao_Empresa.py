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
df1 = pd.read_pickle('pages/dflimpo.pkl')
df = df1.copy()
#print(df.dtypes)

st.set_page_config( page_title='Visão Empresa', page_icon='📈', layout='wide')
#Funções!
def order_metric(df):
    #1. Quantidade de pedidos por dia.
    df_aux = df.loc[:, ['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
    #Gráfico da questão :
    fig = pl.bar(df_aux, x='Order_Date', y='ID')
    return fig

def traffic_order_share(df): #identar
    #Distribuição dos pedidos por tipo de tráfego. (pizza)
    df_aux = (df.loc[:, ['ID', 'Road_traffic_density']].groupby(['Road_traffic_density'])
                                                                        .count()
                                                                        .reset_index())
    df_aux['percent'] = (df_aux['ID'] /(df_aux['ID']).sum())
    fig = pl.pie(df_aux, values = 'percent', names = 'Road_traffic_density')
    return fig

def traffic_order_city(df):
     #Comparação do volume de pedidos por cidade e tipo de tráfego.
     #Gráfico de bolhas
     df_aux = (df.loc[:, ['City', 'ID', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density'])
                                                                .count()
                                                                .reset_index())
     fig = pl.scatter(df_aux, x='City', y='Road_traffic_density', size = 'ID', color= 'City')  
     return fig

def order_by_week(df):
    df['week_of_year'] = df['Order_Date'].dt.strftime('%U')
    df['week_of_year'] = df['week_of_year'].astype(int)
    df_aux = df.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
    #Gráfico da questão :
    fig = pl.line(df_aux, x='week_of_year', y='ID')
    return fig

def order_share_by_week(df):
    df['week_of_year'] = df['Order_Date'].dt.strftime('%U')
    df['week_of_year'] = df['week_of_year'].astype(int)
    # Quantidade de pedidos por semana / Número único de entregadores por semana - juntar os dois dataframes.
    df_aux01 = df.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
    df_aux02 = df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()
    df_aux = pd.merge(df_aux01, df_aux02, how='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID']/df_aux['Delivery_person_ID']
    #Gráfico da questão :
    fig = pl.line(df_aux, x='week_of_year', y='ID')
    return fig 

def country_maps(df):
    df['Restaurant_latitude'] = df['Restaurant_latitude']/1000000
    df['Restaurant_longitude'] = df['Restaurant_longitude']/1000000
    df['Delivery_location_latitude'] = df['Delivery_location_latitude']/1000000
    df['Delivery_location_longitude'] = df['Delivery_location_longitude']/1000000
    df['distance'] = df.apply(
        lambda row: haversine(
            (row['Restaurant_latitude'], row['Restaurant_longitude']), 
            (row['Delivery_location_latitude'], row['Delivery_location_longitude'])), 
            axis=1) #o axis fica fora do haversine!
    df_aux = df.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'City', 'Road_traffic_density', 'distance']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    #montando o mapa
    #Parte dos pinos:
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                    location_info['Delivery_location_longitude']], popup = location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static(map, width=1024, height=600)
    return None 

#Cor da Barra Lateral: Usa CSS dentro do markdown!
#----------------------------------
#Layout - STREAMLIT
st.header("MARKETPLACE - VISÃO CLIENTE")
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

# ---------- IMAGEM NA SIDEBAR ----------
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


#---Criando as tabs:
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', ' Visão Tática', ' Visão Geográfica'])

with tab1:
    with st.container(): #primeiro container
        fig = order_metric(df)
        st.markdown('# Pedidos por Dia')
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        col1, col2 = st.columns(2) #para criar duas colunas
        with col1:
            fig = traffic_order_share(df)
            st.header('Pedidos por Tipo de Tráfego')
            st.plotly_chart(fig, use_container_width=True) 
    
        with col2: 
            fig = traffic_order_city(df)
            st.header('Pedidos por Cidade e Tipo de Tráfego')
            st.plotly_chart(fig, use_container_width=True)   
                    
with tab2:
    with st.container():
        st.header('Análise Semanal')
        st.markdown("---")
        st.markdown('### Quantidade de pedidos por semana')
        fig = order_by_week(df)
        st.plotly_chart(fig, use_container_width=True, key='grafico_1')
    
    with st.container():
        st.markdown('### Quantidade de pedidos por entregador e por semana')
        fig = order_share_by_week(df)
        st.plotly_chart(fig, use_container_width=True, key="grafico_2")
    
with tab3:
    st.header('Mapa Geográfico dos Restaurantes')
    # A localização central de cada cidade por tipo de tráfego.
    #na distancia = mediana, pois ela está na base de dados.
    fig = country_maps(df)
    







#Exercícios - Visão RESTAURANTES!
#1. A quantidade de entregadores únicos.
#df_aux = df.loc[:, ['Delivery_person_ID']].count()
#print(df_aux)

#2.A distância média dos resturantes e dos locais de entrega.
#df['Restaurant_latitude'] = df['Restaurant_latitude']/1000000
#df['Restaurant_longitude'] = df['Restaurant_longitude']/1000000
#df['Delivery_location_latitude'] = df['Delivery_location_latitude']/1000000
#df['Delivery_location_longitude'] = df['Delivery_location_longitude']/1000000
#df['distance'] = df.apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
#                                              (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)
#print(df['distance'])
         #ou #print(df['distance'].mean())

#3: O tempo médio e o desvio padrão de entrega por cidade.
#Usar a função split por meio do apply e do lambda.
#df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
#df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
#df_aux = (df.loc[:, ['City', 'Time_taken(min)']].groupby(['City'])
#                                                .agg({'Time_taken(min)':['mean', 'std']}))
#Renomear os nomes das colunas para resetar os index:
#renomear:
#df_aux.columns = ['delivery_avg', 'delivery_std']
#df_aux = df_aux.reset_index()
#print(df_aux)

#4.O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
#df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
#df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
#df_aux = (df.loc[:, ['City', 'Type_of_order', 'Time_taken(min)']].groupby(['City', 'Type_of_order'])
#                                                                   .agg({'Time_taken(min)': ['mean', 'std']}))
#df_aux.columns = ['Tempo Médio', 'Desvio Padrão do Tempo']
#df_aux = df_aux.reset_index()
#print(df_aux)

#5.O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
#df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
#df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
#df = df.rename(columns=({'Road_traffic_density': 'Densidade'})) #se der problema, trocar densidade por R.Traf. Density
#df_aux = (df.loc[:, ['Time_taken(min)', 'City', 'Densidade']].groupby(['City', 'Densidade'])
#                                                              .agg({'Time_taken(min)': ['mean', 'std']}))
#df_aux.columns = ['Tempo Médio', 'Desvio Padrão']
#df_aux = df_aux.reset_index()
#print(df_aux)

#5. O tempo médio de entrega durantes os Festivais.
#df = df[df['Festival']!='NaN ' ]
#df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
#df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
#df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).mean().reset_index()
#print(df_aux)










#3.O tempo médio e o desvio padrão de entrega por cidade.
#Retirando o o termo '(min)_' da coluna Time_Taken 

