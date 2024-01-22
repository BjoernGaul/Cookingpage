import streamlit as st
from PIL import Image
import os
import json
import random


#---------------------------Funktions------------------------------

def holeAlleRezepte(ordnerpfad):
    """
    Holt sich die Pfade aller Images aus einem vorgegebenen Ordner
    :param ordnerpfad: Der Ordner, in dem sich die Images befinden
    :return: Gibt eine Liste aller Images (datei) bzw. deren Pfade zurück.
    """
    # Alle Dateien im Ordner auflisten; In "dateien" liegen jetzt die Pfade aller Images und Bilder
    dateien = os.listdir(ordnerpfad)

    # Wir wollen aber die Dateien mit ihrem relativen Pfad haben
    for i in range(len(dateien)):
        dateien[i] = os.path.join(ordnerpfad, dateien[i])
    return dateien

def getRecipe(rezeptPfad):
    """
    Liest ein Rezept ein. Der Pfad zu dem Rezept wird als Parameter übergeben
    :param rezeptPfad: Pfad zu dem Rezept, dass eingelesen werden soll.
    :return: Ein Dictionary mit dem eingelesenen Rezept
    """
    rezeptDict = {}
    rezeptDict['Name'] = os.path.splitext(os.path.basename(rezeptPfad))[0]
    rezeptartFolgtSwitch = False
    zutatenFolgenSwitch = False  # Wenn der Schalter gesetzt ist, dann folgt gerade die Zutatenliste
    rezeptTextFolgtSwitch = False
    sonstigesFolgtSwitch = False
    rezeptartList = []
    zutatenListe = []
    zubereitungstext = ''
    sonstiges = ''
    # Öffne den Inhalt der Datei/Rezepts und lies zeilenweise die Zeilen des Rezeptes ein
    with open(rezeptPfad, encoding='utf-8') as file:
        for zeile in file:
            if zeile[0] == '#':  # wir haben eine Überschrift;ein Hashtag
                zeile = zeile.strip('#').strip()  # Bereinigte Überschrift
                if zeile == 'Rezeptart':
                    rezeptartFolgtSwitch = True
                if zeile == 'Zutaten':  # es folgen die Zutaten
                    rezeptartFolgtSwitch = False
                    zutatenFolgenSwitch = True
                    continue
                if zeile == 'Zubereitung':
                    rezeptTextFolgtSwitch = True
                    zutatenFolgenSwitch = False
                    continue
                if zeile == 'Zusatzdaten':
                    rezeptTextFolgtSwitch = False
                    sonstigesFolgtSwitch = True
                    continue
            if rezeptartFolgtSwitch == True:
                rezeptartList.append(zeile.replace('\n',''))
            if zutatenFolgenSwitch == True:
                zeile = zeile.strip()
                zutatenListe.append(zeile)
            if rezeptTextFolgtSwitch == True:
                zubereitungstext += zeile
            if sonstigesFolgtSwitch == True:
                sonstiges += zeile

        # Hänge alles in das Dictionary ein
        rezeptDict['Rezeptart'] = rezeptartList
        rezeptDict['Zutaten'] = zutatenListe
        rezeptDict['Zubereitung'] = zubereitungstext
        rezeptDict['Sonstiges'] = sonstiges
    return rezeptDict


def relst():
    # Ordnerpfad angeben; hier geben wir einen relativen Pfad an
    ordnerpfad = './recipes'

    bilderLst = []
    rezepteLst = []
    rezeptePfade = []
    dateien = holeAlleRezepte(ordnerpfad)
    sortedrecipes = []

    # Trenne die Bilder von den Rezepten
    if 'bilderLst' not in st.session_state:
        for datei in dateien:
            if datei[-4:] == '.jpg' or datei[-4:] == '.png' or datei[-5:] == '.webp':
                bilderLst.append(datei)
            if datei[-4:] == '.txt':
                rezeptePfade.append(datei)
        st.session_state.bilderLst = bilderLst

    # Rezepte auslesen
    if 'rezepteLst' not in st.session_state:
        for datei in rezeptePfade:
            rezeptDict = getRecipe(datei)
            rezepteLst.append(rezeptDict)
        # print(f'datei{rezepteLst}')
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

relst()

if 'rezepteLst' in st.session_state:
    rezepteLst = st.session_state.rezepteLst

if 'bilderLst' in st.session_state:
    bilderLst = st.session_state.bilderLst


def change_recipe(*recipe):
    st.session_state['recipe'] = recipe

def resetsessionweek():
    #reset für wochenliste
    if 'rezeptindtage' in st.session_state:
        del st.session_state.rezeptindtage

def weeklistcol(tage):
    #Wochenliste nach angegebenen Tagen
    #columns
    col1, col2 = st.columns(2)
    #check ob bereits wlist erstellt wurde und ob gleiche länge vorhanden ist
    if 'rezeptindtage' not in st.session_state:
        st.session_state.rezeptindtage = random.sample(range(len(rezepteLst)), tage)
    if len(st.session_state.rezeptindtage) != tage:
        st.session_state.rezeptindtage = random.sample(range(len(rezepteLst)),tage)
    #vereinfachung der variable
    rezeptindtage = st.session_state.rezeptindtage
    #rezepte auslesen

    for res in rezeptindtage:
        with col1:
            recipe = rezepteLst[res]
            #buttons für jeden tag und button zu rezept erstellen
            st.button(f'Tag {rezeptindtage.index(res) + 1}: {recipe["Name"].replace("_", " ")}', on_click=change_recipe, args=(res,))
        with col2:
            st.button('Wechsel Rezept',on_click=change_me, key=recipe["Name"], args=(res,))

def change_me(*recipe):
    rezeptindtage = st.session_state.rezeptindtage
    rezepteLst = st.session_state.rezepteLst
    rezeptecopy = rezepteLst.copy()
    rezept = recipe[0]
    for rez in rezeptindtage:
        if rezepteLst[rez] in rezeptecopy:
            rezeptecopy.remove(rezepteLst[rez])
    rezind = rezeptindtage.index(rezept)
    rezeptindtage[rezind] = rezepteLst.index(random.sample(rezeptecopy, 1)[0])
    st.session_state.rezeptindtage = rezeptindtage



def weeklist():
    #wochenliste initialisierung
    tage = st.slider('Wieviele Tage wollen sie kochen?', min_value=1, max_value=7, value=5)
    weeklistcol(tage)
    if st.button('Neue Rezepte'):
        resetsessionweek()
        st.rerun()

#floatcheck
def is_float(string):
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False
#Menge auf Personenzahl ändern
# Menge aus Zutatenliste auslesen und auf Personezahl anpassen
def menge(personenzahl, zutaten):
    zutadic = {}
    for zutat in zutaten:
        ind = zutaten.index(zutat)
        zl = zutat.split(' ',1)
        anzahl = zl[0]
        #print(anzahl)
        zutat = zutat.replace(anzahl, '')
        menge = anzahl.replace(',', '.')

        if is_float(menge):
            menge = float(menge) / 4 * personenzahl
            zutadic[zutat] = round(menge,2)
        else:
            continue
    #print(zutaten)
    return zutadic

#Rezeptsuche
def search_recipe(keyword):
    #Suchliste
    searchLst = []
    rezepteLst = st.session_state.rezepteLst
    #sessionstate reset
    if 'recipe' in st.session_state:
        del st.session_state.recipe
    # Überprüfe, ob das Schlüsselwort gefunden wurde

    for recipe in rezepteLst:
        if keyword.lower() in str(recipe['Name']).lower() or keyword.lower() in str(recipe['Rezeptart']).lower():
            searchLst.append(recipe)
    return searchLst


def einkaufslst():

    if 'einkaufslst' not in st.session_state:
        st.session_state.einkaufslst = {}

    if 'zutaten' in st.session_state:
        zutaten = st.session_state.zutaten
        einkaufsdic = st.session_state.einkaufslst
        print(einkaufsdic)
        for zutat in zutaten:
            if zutat in einkaufsdic:
                einkaufsdic[zutat] += zutaten[zutat]
            else:
                einkaufsdic[zutat] = (zutaten[zutat])
        st.session_state.einkaufslst = einkaufsdic
        print(einkaufsdic)

#rezeptausgabe
def recipeprint(recipe):

    recipeindex = recipe[0]
    #print(recipeindex)
    zutatenLst = rezepteLst[recipeindex]['Zutaten']

    st.title(rezepteLst[recipeindex]['Name'].replace('_',' '))

    # Lade das Bild des Gerichts
    dish_image = Image.open(bilderLst[recipeindex])
    st.image(dish_image)
    st.write(str(rezepteLst[recipeindex]['Rezeptart']).replace('Rezeptart','').replace("'",'')
            .replace(',','').replace('[','').replace(']',''))

    # Personenzahl
    personenzahl = st.slider('Personenzahl', min_value=1, max_value=12, value=4)
    zutaten = menge(personenzahl, zutatenLst)
    st.session_state.zutaten = zutaten

    col1, col2 = st.columns(2)
    # Schreibe den Text des Rezepts
    col1.header('Zutaten:')
    with col1:
        for zutat in zutaten:
            st.write(str(zutaten[zutat])+zutat)


        if st.button('Zur Einkaufsliste Hinzufügen'):
            einkaufslst()



    col2.header('Anleitung:')
    with col2:
        st.write(rezepteLst[recipeindex]['Zubereitung'])


    st.header('Zusatzdaten')
    st.text(rezepteLst[recipeindex]['Sonstiges'])




def showrecipelst():
    for recipe in rezepteLst:
        # print(recipe['Name'])
        rezept = rezepteLst.index(recipe)
        # print(f'test2{rezept}')
        st.button(recipe['Name'].replace('_', ' ') + ', Kategorien: ' + str(recipe['Rezeptart'])
                  .replace('Rezeptart', '').replace("'", '').replace(',', '')
                  .replace('[', '').replace(']', ''), on_click=change_recipe, args=(rezept,))

def resetsession():
    del st.session_state.recipe

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
def rand3menue():
    #3 Gänge Menü
    menuelst3 = []

    # Zufällige Vorspeise
    vorspeisen = [recipe for recipe in rezepteLst if 'Vorspeise' in recipe['Rezeptart']]
    selected_vorspeise = random.choice(vorspeisen)
    menuelst3.append(selected_vorspeise)

    # Zufällige Hauptspeise
    hauptspeisen = [recipe for recipe in rezepteLst if 'Hauptspeise' in recipe['Rezeptart']]
    selected_hauptspeise = random.choice(hauptspeisen)
    menuelst3.append(selected_hauptspeise)

    # Zufällige Nachspeise
    nachspeisen = [recipe for recipe in rezepteLst if 'Nachspeise' in recipe['Rezeptart']]
    selected_nachspeise = random.choice(nachspeisen)
    menuelst3.append(selected_nachspeise)

    return menuelst3

def searchlstbuttons(search_lst):
    if 'rezepteLst' in st.session_state:
        rezepteLst = st.session_state.rezepteLst
        for recipe in search_lst:
            #print(recipe['Name'])
            rezept = rezepteLst.index(recipe)
            #print(f'test2{rezept}')
            st.button(recipe['Name'].replace('_',' '),on_click=change_recipe, args=(rezept,))



def printZutatenRezept(rezept):
    """
    Hilfsfunktion. Druckt die Zutaten eines Rezeptes auf der Konsole aus
    :param rezept: Nummer des Rezeptes, dass ausgegeben werden soll
    :return: nichts
    """
    print(f"Zutaten: {rezepteLst[rezept]['Name'][:-4]}")  #

    zutatenliste = rezepteLst[rezept]['Zutaten']
    for zutat in zutatenliste:
        print(zutat)


def printZubereitung(rezept):
    """
    Gibt die Zubereitung eines Rezeptes aus.
    :param rezept: Nummer des Rezeptes, dessen Zubereitung ausgegeben werden soll
    :return: nichts
    """
    print(f"Zubereitung: {rezepteLst[rezept]['Name'][:-4]}")
    anweisungen = rezepteLst[rezept]['Zubereitung']
    print(anweisungen)


def printSonstiges(rezept):
    """
    Gibt die sonstigen Informationen eines Rezeptes aus.
    :param rezept: Nummer des Rezeptes, dessen sonstige Informationen ausgegeben werden sollen.
    :return: nichts
    """
    sonstiges = rezepteLst[rezept]['Sonstiges']
    print(sonstiges)
