import os
import streamlit as st
from streamlit_lottie import st_lottie
import json

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_coding = load_lottiefile("./slider.json")
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

# Nach einem Titel fragen
title = st.text_input("Gib einen Titel für dein Rezept ein:")

# Text Input erstellen und die Höhe anpassen
user_input1 = st.text_area(
    "Rezeptart (Fleisch, Vegetarisch, Vegan, Kochen, Backen, Vorspeise, Hauptspeise, Nachspeise, Fisch, Ungekocht, Schnell, Edel):")
user_input2 = st.text_area("Gib hier die Zutatenliste ein", height=200)
user_input3 = st.text_area("Gib hier die Informationen für die Zubereitung ein:", height=200)
user_input4 = st.text_area("Gib hier die Zusatzdaten ein (Arbeitszeit, Koch-Backzeit, Gesamtzeit):", height=200)

# File Uploader für das Bild hinzufügen
uploaded_image = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

# Button hinzufügen, um die eingegebenen Texte und das Bild zu speichern
if st.button("Speichern"):
    # Überprüfen, ob alle Inputs ausgefüllt sind
    if not title or not user_input1 or not user_input2 or not user_input3 or not user_input4 or not uploaded_image:
        st.warning("Bitte fülle alle Felder aus und lade ein Bild hoch, bevor du das Rezept speicherst.")
    else:
        # Pfad zum Ordner, in dem die Dateien gespeichert werden sollen
        folder_path = "./recipes"  # Ersetze dies durch den tatsächlichen Pfad
        image_folder_path1 = "./Images"  # Ersetze dies durch den tatsächlichen Pfad für das erste Bild
        image_folder_path2 = "./recipes"  # Ersetze dies durch den tatsächlichen Pfad für das zweite Bild

        # Dateipfad erstellen
        file_path = f"{folder_path}/{title}.txt"
        image_path1 = f"{image_folder_path1}/{title}.jpg"
        image_path2 = f"{image_folder_path2}/{title}.jpg"

        # Überprüfen, ob die Dateien bereits existieren
        if os.path.exists(file_path) or os.path.exists(image_path1) or os.path.exists(image_path2):
            st.warning(f"Rezept mit dem Titel '{title}' existiert bereits.")
        else:
            # Texte und Bild in die Dateien schreiben
            with open(file_path, "w") as file:
                file.write(
                    f"{title}\n\n#Rezeptart\n{user_input1}\n\n#Zutaten\n{user_input2}\n\n#Zubereitung\n{user_input3}\n\n#Zusatzdaten\n{user_input4}\n"
                )

            with open(image_path1, "wb") as image_file1, open(image_path2, "wb") as image_file2:
                image_file1.write(uploaded_image.getvalue())
                image_file2.write(uploaded_image.getvalue())

            st.success(f"Ihr Rezept wurde erfolgreich gespeichert.")





