import streamlit as st
from PIL import Image

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

/* sidebar espaçamento */
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

st.sidebar.markdown("## CURRY COMPANY -  O Delivery mais rápido da cidade!")
st.sidebar.markdown(
    """
    Feito por **Guilherme G. Guimarães**
    <div style="text-align:center;">

    <a href="https://www.linkedin.com/in/guilherme-gonçalves-guimarães-5a407a281/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="40">
    </a>

    <a href="https://www.instagram.com/gui2021br/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="40">
    </a>

    <a href="https://wa.me/5543991785400" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="40">
    </a>

    </div>
    """,
unsafe_allow_html=True
 )
st.sidebar.markdown("---")
#image_path = r"C:\Users\Guilherme G\Desktop\reposs\curry_company\logo_curry.png"
image = Image.open('logo_curry.png')
st.sidebar.image(image)

st.container()
st.markdown(
    """
    <h2 style="color:#E50914; text-align:center;">
    Dashboard da Curry Company by Guilherme Guimarães
    - 
    <a href="https://www.linkedin.com/in/guilherme-gonçalves-guimarães-5a407a281/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30">
    </a>

    <a href="https://www.instagram.com/gui2021br/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="30">
    </a>

    <a href="https://wa.me/5543991785400" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="30">
    </a>

    </div>
    </h2>
    <div style="text-align:center;">
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    #### Este Dashboard foi construído para acompanhar as métricas de crescimento de Entregadores e Restaurantes.
    ## Como utilizar esse Growth Dashboard?

    ### - Visão Empresa:
    #####    - Visão Gerencial: Métricas gerais de comportamento.
    #####   - Visão Tática: Indicadores semanais de crescimento.
    #####    - Visão Geográfica: Insights de geolocalização.
    ### - Visão Entregador:
    #####    - Acompanhamento dos indicadores semanais de crescimento
    ### - Visão Restaurante:
    #####    - Indicadores semanais de crescimento dos restaurantes
     """
    )


st.set_page_config(
    page_title='Home',
    page_icon='📈'
)

