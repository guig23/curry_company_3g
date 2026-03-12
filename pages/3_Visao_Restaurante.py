# Bibliotecas - libraries
import streamlit as st 
import pandas as pd
import plotly.express as pl
from haversine import haversine 
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
import folium
import numpy as np 
from streamlit_folium import folium_static
#Carregar o arquivo 
df1 = pd.read_pickle('pages/dflimpo.pkl')
df = df1.copy()

st.set_page_config( page_title='Visão Restaurante', page_icon='🍟', layout='wide')

#----------------------------------
#Layout - STREAMLIT
#Cor da Barra Lateral: Usa CSS dentro do markdown!

#----------------------------------
#Funções:
def haversine_distance(df):
    df['Restaurant_latitude'] = df['Restaurant_latitude']/1000000
    df['Restaurant_longitude'] = df['Restaurant_longitude']/1000000
    df['Delivery_location_latitude'] = df['Delivery_location_latitude']/1000000
    df['Delivery_location_longitude'] = df['Delivery_location_longitude']/1000000
    df['distance'] = df.apply(
        lambda row: haversine(
            (row['Restaurant_latitude'], row['Restaurant_longitude']), 
            (row['Delivery_location_latitude'], row['Delivery_location_longitude'])), 
            axis=1)
    distancia_media = np.round(df.loc[:, 'distance'].mean(), 1)
    return  distancia_media

def avg_festival_yes(df):
    df = df[df['Festival']!='NaN ']
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'desviopadrao']
    df_aux = df_aux.reset_index()
    df_aux= np.round(df_aux.loc[df_aux['Festival'] == 'Yes ', 'avg_time'], 1) #virou só um número com esse loc.
    return df_aux

def desvio_padrao_yes(df):
    df = df[df['Festival']!='NaN ']
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'desviopadrao']
    df_aux = df_aux.reset_index()
    df_aux= np.round(df_aux.loc[df_aux['Festival'] == 'Yes ', 'desviopadrao'], 1) #virou só um número com esse loc.
    return df_aux

def time_without_festival(df):
    df = df[df['Festival']!='NaN ']
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'desviopadrao']
    df_aux = df_aux.reset_index()
    df_aux= np.round(df_aux.loc[df_aux['Festival'] == 'No ', 'avg_time'], 1) #virou só um número com esse loc.
    return df_aux

def desvio_without_festival_2(df):
    df = df[df['Festival']!='NaN ']
    df_aux = df.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'desviopadrao']
    df_aux = df_aux.reset_index()
    df_aux= np.round(df_aux.loc[df_aux['Festival'] == 'No ', 'desviopadrao'], 1) #virou só um número com esse loc.
    return df_aux

def plot_barra(df):
    df_aux = (df.loc[:, ['City', 'Time_taken(min)']].groupby(['City'])
                                                    .agg({'Time_taken(min)':['mean', 'std']}))
    #Renomear os nomes das colunas para resetar os index:
    #renomear:
    df_aux.columns = ['delivery_avg', 'delivery_std']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['delivery_avg'], error_y=dict(type='data', array=df_aux['delivery_std'])))
    fig.update_layout(barmode='group')
    return fig

def dataframe_avg_and_std(df):
    df_aux = df.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    return df_aux

def distance_lat_long(df):
    df['Restaurant_latitude'] = df['Restaurant_latitude']/1000000
    df['Restaurant_longitude'] = df['Restaurant_longitude']/1000000
    df['Delivery_location_latitude'] = df['Delivery_location_latitude']/1000000
    df['Delivery_location_longitude'] = df['Delivery_location_longitude']/1000000
    df['distance'] = df.apply(
        lambda row: haversine(
            (row['Restaurant_latitude'], row['Restaurant_longitude']), 
            (row['Delivery_location_latitude'], row['Delivery_location_longitude'])), 
            axis=1) #o axis fica fora do haversine!
    avg_distance = df.loc[:, ['City', 'distance']].groupby(['City']).mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels= avg_distance['City'], values=avg_distance['distance'], pull=[0,0.1, 0], marker=dict(colors=['red', 'blue', 'green']))])
    return fig

def plot_avg_std_density(df): 
    df_aux = df.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = pl.sunburst(df_aux, path=['City', 'Road_traffic_density'], values = 'avg_time',
                    color='std_time', color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig 

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

#Limpeza extra:
df['Time_taken(min)'] = df['Time_taken(min)'].astype(str).apply(lambda x: x.split('(min)')[1])
df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)

#Layout - STREAMLIT
st.header("CURRY COMPANY - VISÃO RESTAURANTES")
tab1, tab2, tab3 = st.tabs(['Visão Gerencial das Entregas', '-', '-'])
with tab1:
    with st.container():
        st.markdown("<h2 style='text-align: center;'>Métricas Gerais</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5, col6 = st.columns(6, gap = 'medium')
        with col1: 
            total_entregadores = (df.loc[:, 'Delivery_person_ID'].nunique())
            col1.metric('Entregadores', total_entregadores)
        with col2:
            fig = haversine_distance(df)
            col2.metric('Tempo S.F:', fig)
        with col3:
            fig = avg_festival_yes(df)
            col3.metric('AVG Time:', fig)
        with col4:
            fig = desvio_padrao_yes(df)
            col4.metric('Desvio P. C.F:', fig)

        with col5:
           fig = time_without_festival(df)
           col5.metric('Tempo S.F', fig)
        with col6:
            fig = desvio_without_festival_2(df)
            col6.metric('Desvio P. S.F:', fig)
            
    with st.container():
        st.markdown("""___""")
        st.markdown("<h2 style='text-align: center;'>Tempo e Desvio Padrão por Região da Cidade</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig = plot_barra(df)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = dataframe_avg_and_std(df)
            st.dataframe(fig)
            
    with st.container():
        st.markdown("""___""")
        st.markdown("<h2 style='text-align: center; '>Distribuição de Tempo</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig = distance_lat_long(df)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = plot_avg_std_density(df)
            st.plotly_chart(fig, use_container_width=True)    
   
        





#Exercícios - Visão empresa
#1. Quantidade de pedidos por dia.
#df_aux = df.loc[:, ['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
#print(df_aux)
#Gráfico da questão :
#fig = pl.bar(df_aux, x='Order_Date', y='ID')
#fig.show()

#2. Quantidade de pedidos por semana.
#df['week_of_year'] = df['Order_Date'].dt.strftime('%U')
#df['week_of_year'] = df['week_of_year'].astype(int)
# Quantidade de pedidos por semana / Número único de entregadores por semana - juntar os dois dataframes.
#df_aux01 = df.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
#df_aux02 = df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()
#df_aux = pd.merge(df_aux01, df_aux02, how='inner', on='week_of_year')
#df_aux['order_by_deliver'] = df_aux['ID']/df_aux['Delivery_person_ID']
#print(df_aux)
#Gráfico da questão :
#fig = pl.line(df_aux, x='week_of_year', y='ID')
#fig.show()

#3. Distribuição dos pedidos por tipo de tráfego. (pizza)
#df_aux = (df.loc[:, ['ID', 'Road_traffic_density']].groupby(['Road_traffic_density'])
#                                                    .count().
#                                                    reset_index())
#df_aux['percent'] = (df_aux['ID'] /(df_aux['ID']).sum())
#fig = pl.pie(df_aux, values = 'percent', names = 'Road_traffic_density')
#fig.show()

#4. Comparação do volume de pedidos por cidade e tipo de tráfego.
#Gráfico de bolhas
#df_aux = (df.loc[:, ['City', 'ID', 'Road_traffic_density']]
#             .groupby(['City', 'Road_traffic_density'])
#             .count()
#             .reset_index())
#print(df_aux)
#fig = pl.scatter(df_aux, x='City', y='Road_traffic_density', size = 'ID', color= 'City')
#fig.show()

#5. A localização central de cada cidade por tipo de tráfego.
#na distancia = mediana, pois ela está na base de dados.
#df['Restaurant_latitude'] = df['Restaurant_latitude']/1000000
#df['Restaurant_longitude'] = df['Restaurant_longitude']/1000000
#df['Delivery_location_latitude'] = df['Delivery_location_latitude']/1000000
#df['Delivery_location_longitude'] = df['Delivery_location_longitude']/1000000
#df['distance'] = df.apply(
#    lambda row: haversine(
#        (row['Restaurant_latitude'], row['Restaurant_longitude']), 
#        (row['Delivery_location_latitude'], row['Delivery_location_longitude'])), 
#        axis=1) #o axis fica fora do haversine!
#df_aux = df.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'City', 'Road_traffic_density', 'distance']].groupby(['City', 'Road_traffic_density']).median().reset_index()
#print(df_aux)
#montando o mapa
#Parte dos pinos:
#map = folium.Map()
#for index, location_info in df_aux.iterrows():
#    folium.Marker([location_info['Delivery_location_latitude'],
#                   location_info['Delivery_location_longitude']], popup = location_info[['City', 'Road_traffic_density']]).add_to(map)
#    map.save('mapa.html')

#webbrowser.open('mapa.html')
