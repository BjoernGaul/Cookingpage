import streamlit as st
from st_clickable_images import clickable_images
import base64
from pages.Functions.functions import holeAlleRezepte
from pages.Functions.functions import relst
from streamlit_extras.switch_page_button import switch_page

folder = "./recipes"
images = []
relst()
if 'rezepteLst' in st.session_state:
    rezepteLst = st.session_state.rezepteLst


files = holeAlleRezepte(folder)

for file in files:
    if file[-4:] == '.jpg' or file[-4:] == '.png' or file[-5:] == '.webp':
        with open(file, 'rb')as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")


clicked = clickable_images(
    images
    ,
    titles=[f"Image #{str(i)}" for i in range(5)],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "200px"},
)


if clicked > -1:
    st.session_state.recipe = (clicked,)
    switch_page('rezepte')