import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
import os
from pages.Functions.functions import holeAlleRezepte
from pages.Functions.functions import getRecipe
#------------------------Grundfunktionen------------------------------
# Ordnerpfad angeben; hier geben wir einen relativen Pfad an
ordnerpfad = './recipes'

bilderLst = []
rezepteLst = []
rezeptePfade = []
dateien = holeAlleRezepte(ordnerpfad)
sortedrecipes = []

# Trenne die Bilder von den Rezepten

for datei in dateien:
    if datei[-4:] == '.jpg' or datei[-4:] == '.png' or datei[-5:] == '.webp':
        bilderLst.append(datei)
    if datei[-4:] == '.txt':
        rezeptePfade.append(datei)
st.session_state.bilderLst = bilderLst

#Rezepte auslesen

for datei in rezeptePfade:
    rezeptDict = getRecipe(datei)
    rezepteLst.append(rezeptDict)
#print(f'datei{rezepteLst}')
st.session_state.rezepteLst = rezepteLst

# Check, ob es so viele Bilder wie Texte gibt:
for bild in bilderLst:
    if bild[:-4] + '.txt' in rezeptePfade or bild[:-5] + '.txt' in rezeptePfade:
        continue
    else:
        print(f"Zu dem Bild: {bild} gibt es keinen Text")
        bilderLst.remove(bild)

if len(bilderLst) != len(rezepteLst):
    print("Rezeptdateien überprüfen. Anzahl stimmt nicht überein.")




#----------------------Homepage anzeige-------------------

# Setze die Seite-Konfiguration als erste Zeile
st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)
ordner_pfad = './recipes'
dateien = os.listdir(ordner_pfad)
textdateien = [datei for datei in dateien if datei.endswith('.txt')]
anzahl_rezepte = len(textdateien)
# Funktion zum Laden von Lottie-Dateien


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Funktion zum Laden von Lottie-URLs
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


title = "Welcome to Chefblob"
text = f"Chefblob wurde von der Schülergruppe Björn, Leon und Sebastian ins Leben gerufen und präsentiert stolz eine Auswahl von derzeit {anzahl_rezepte} Rezepten. Wir setzen jedoch fortlaufend daran, diese Sammlung zu erweitern. Zusätzlich haben Nutzer die Möglichkeit, eigene Rezepte beizusteuern. Chefblob ist eine zuverlässige Ressource für Hobbyköche, die sorgfältig ausgewählte Rezepte und Anleitungen bietet."

# Dein bisheriger Code mit den übersetzten Texten
st.sidebar.success("Select a page above.")
st.image('./MicrosoftTeams-image.png', use_column_width=True)

lottie_coding = load_lottiefile("./Recipe.json")

st.markdown(f"<h1 style='text-align: center; font-size: 52px;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)

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
