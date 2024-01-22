import streamlit as st
import random
from PIL import Image
from pages.Functions.functions import recipeprint
from pages.Functions.functions import weeklist
from pages.Functions.functions import relst


#------------------------Main site---------------------------------
st.header('📝Wochenliste')

#recepte auslesen
relst()

if 'rezepteLst' in st.session_state:
    rezepteLst = st.session_state.rezepteLst
if 'bilderLst' in st.session_state:
    bilderLst = st.session_state.bilderLst


weeklist()

#rezepte ausgeben
if 'recipe' in st.session_state:
    # print(st.session_state.recipe)
    recipeprint(st.session_state.recipe)