import os

# Ordnerpfad angeben; hier geben wir einen relativen Pfad an
ordnerpfad = './recipes'
# Funktionen
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
    zutatenFolgenSwitch = False # Wenn der Schalter gesetzt ist, dann folgt gerade die Zutatenliste
    rezeptTextFolgtSwitch = False
    sonstigesFolgtSwitch = False
    rezeptartList = []
    zutatenListe = []
    zubereitungstext = ''
    sonstiges = ''
    # Öffne den Inhalt der Datei/Rezepts und lies zeilenweise die Zeilen des Rezeptes ein
    with open(rezeptPfad, encoding='utf-8') as file:
        for zeile in file:
            if zeile[0] == '#':         # wir haben eine Überschrift;ein Hashtag
                zeile = zeile.strip('#').strip()   # Bereinigte Überschrift
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
                rezeptartList.append(zeile)
            if zutatenFolgenSwitch == True:
                zeile = zeile.strip()
                zutatenListe.append(zeile)
            if rezeptTextFolgtSwitch == True:
                zubereitungstext += zeile
            if sonstigesFolgtSwitch == True:
                sonstiges += zeile
                
        #Menge aus Zutatenliste auslesen und auf Personezahl anpassen
        for zutat in zutatenListe:
            ind = zutatenListe.index(zutat)
            menge = ''
            for s in zutat:
                if s.isdigit() or s == '.':
                    zutat = zutat.strip(s)
                    menge += s
                elif s == '':
                    break
            if menge == '':
                continue
            menge = float(menge)/4*personenzahl
            zutatenListe.pop(ind)
            zutatenListe[ind] = str(menge) + zutat
        print(zutatenListe)


        # Hänge alles in das Dictionary ein
        rezeptDict['Rezeptart'] = rezeptartList
        rezeptDict['Zutaten'] = zutatenListe
        rezeptDict['Zubereitung'] = zubereitungstext
        rezeptDict['Sonstiges'] = sonstiges
    return rezeptDict

#Images Sortieren
def recipesort(rezepte):
    Fleisch = [recipe for recipe in rezepte if 'fleisch' in recipe.lower()]
    Vegetarisch = [recipe for recipe in rezepte if 'vegetarisch' in recipe.lower()]
    Vegan = [recipe for recipe in rezepte if 'vegan' in recipe.lower()]
    Kochen = [recipe for recipe in rezepte if 'kochen' in recipe.lower()]
    Backen = [recipe for recipe in rezepte if 'backen' in recipe.lower()]
    Vorspeise = [recipe for recipe in rezepte if 'vorspeise' in recipe.lower()]
    Hauptspeise = [recipe for recipe in rezepte if 'hauptspeise' in recipe.lower()]
    Nachspeise = [recipe for recipe in rezepte if 'nachspeise' in recipe.lower()]
    Fisch = [recipe for recipe in rezepte if 'fisch' in recipe.lower()]
    return Fleisch, Vegetarisch, Vegan, Kochen, Backen, Vorspeise, Hauptspeise, Nachspeise, Fisch


def printZutatenRezept(rezept):
    """
    Hilfsfunktion. Druckt die Zutaten eines Rezeptes auf der Konsole aus
    :param rezept: Nummer des Rezeptes, dass ausgegeben werden soll
    :return: nichts
    """
    print(f"Zutaten: {rezepteLst[rezept]['Name'][:-4]}") #

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


#------------ Hier folgt das Hauptprogramm------------------
personenzahl = 10
bilderLst = []
rezepteLst = []
rezeptePfade = []
dateien = holeAlleRezepte(ordnerpfad)
sortedrecipes = []

# Trenne die Bilder von den Rezepten
for datei in dateien:
    if datei[-4:] == '.jpg' or datei[-4:] == '.png':
        bilderLst.append(datei)
    if datei[-4:] == '.txt':
        rezeptePfade.append(datei)

# Check, ob es so viele Bilder wie Images gibt:
for bild in bilderLst:
    if bild[:-4] + '.txt' in rezepteLst:
        continue
    else:
        print(f"Zu dem Bild: {bild} gibt es keinen Text")
        bilderLst.remove(bild)

if len(bilderLst) != len(rezepteLst):
    print("Rezeptdateien überprüfen. Anzahl stimmt nicht überein.")

for datei in rezeptePfade:
    rezeptDict = getRecipe(datei)
    rezepteLst.append(rezeptDict)

print("Liste der Rezepte: ", rezepteLst)

#printZutatenRezept(0)
#printZubereitung(0)
#printSonstiges(0)
#printZutatenRezept(1)



