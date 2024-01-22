import streamlit as st
from PIL import Image
import os
from streamlit_lottie import st_lottie
import json
import random
from pages.Functions.functions import search_recipe
from pages.Functions.functions import rand3menue
from pages.Functions.functions import searchlstbuttons
from pages.Functions.functions import recipeprint
from pages.Functions.functions import load_lottiefile
from pages.Functions.functions import relst
# ------------------------Grundfunktionen------------------------------

#Rezepte auslesen
relst()

#Variables
if 'rezepteLst' in st.session_state:
    rezepteLst = st.session_state.rezepteLst
if 'bilderLst' in st.session_state:
    bilderLst = st.session_state.bilderLst

def main():
    search_lst = []
    search_term = st.text_input("Suche nach einem Rezept:")
    #Suche
    if st.button("Suche/Alle Rezepte"):
            search_lst = search_recipe(search_term)
            st.session_state.searchlst = search_lst
            if 'menue3' in st.session_state:
                del st.session_state.menue3

    col1, col2, col3, col4, col5 = st.columns(5)
    #Schnellsuche
    with col1:
        if st.button('Vegetarisch'):
            search_lst = search_recipe('Vegetarisch')
            st.session_state.searchlst = search_lst
            if 'menue3' in st.session_state:
                del st.session_state.menue3
    with col2:
        if st.button('Schnell'):
            search_lst = search_recipe('Schnell')
            st.session_state.searchlst = search_lst
            if 'menue3' in st.session_state:
                del st.session_state.menue3
    with col3:
        if st.button('Edel'):
            search_lst = search_recipe('Edel')
            st.session_state.searchlst = search_lst
            if 'menue3' in st.session_state:
                del st.session_state.menue3
    with col4:
        if st.button('Zufällig'):
            search_lst.append(rezepteLst[random.randint(0,len(rezepteLst))])
            #print(search_lst)
            st.session_state.searchlst = search_lst
            if 'menue3' in st.session_state:
                del st.session_state.menue3
    with col5:
        if st.button("Zufälliges 3-Gänge-Menü"):
            search_lst = rand3menue()
            st.session_state.menue3 = search_lst
            if 'searchlst' in st.session_state:
                del st.session_state.searchlst



    #suche ausgeben
    searchlstbuttons(search_lst)

    #zurück zur suche/menü
    if 'recipe' in st.session_state:
        if st.button('Zurück'):
            del st.session_state.recipe
            if 'menue3' in st.session_state:
                searchlstbuttons(st.session_state.menue3)
            if 'searchlst' in st.session_state:
                searchlstbuttons(st.session_state.searchlst)

    #rezepte ausgeben
    if 'recipe' in st.session_state:
        # print(st.session_state.recipe)
        recipeprint(st.session_state.recipe)


    lottie_coding = load_lottiefile("./Cook.json")
    st_lottie(
        lottie_coding,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=None,
        width=None,
        key=None,
    )

    kategorien = ['Vorspeise', 'Hauptspeise', 'Nachspeise']

    for kategorie in kategorien:
        kategorie_rezepte = [recipe for recipe in rezepteLst if kategorie in recipe['Rezeptart']]

        if kategorie_rezepte:
            st.subheader(f"{kategorie}: {len(kategorie_rezepte)} Rezepte")

        else:
            st.warning(f"Kein Rezept für {kategorie} gefunden.")

if __name__ == "__main__":
    main()
