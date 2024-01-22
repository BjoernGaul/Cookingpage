import os
import streamlit as st
import zipfile

def download_multiple_recipes(recipe_folder, selected_recipes):
    zip_file_name = "Rezeptsliste.zip"
    zip_file_path = os.path.join(recipe_folder, zip_file_name)

    with st.spinner("Erstelle ZIP-Datei..."):
        # Erstelle eine ZIP-Datei und füge ausgewählte Rezepte hinzu
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for selected_recipe in selected_recipes:
                file_path = os.path.join(recipe_folder, selected_recipe + ".txt")
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                zip_file.writestr(selected_recipe + ".txt", content)

        # Lade die erstellte ZIP-Datei herunter
        st.download_button(
            label="Rezepte herunterladen",
            data=open(zip_file_path, 'rb').read(),
            file_name=zip_file_name,
            mime='application/zip',
        )

    # Lösche die ZIP-Datei nach dem Download
    os.remove(zip_file_path)


# Ordner mit Rezepten
recipe_folder = "./recipes"

# Liste der Rezepte im Ordner
recipe_files = [os.path.splitext(f)[0] for f in os.listdir(recipe_folder) if f.endswith('.txt')]

# Streamlit-Anwendung
st.title("⬇️ Rezepte-Download")

# Mehrfachauswahl für die Rezepte
selected_recipes = st.multiselect("Wähle Rezepte aus:", recipe_files)


# Button zum Herunterladen der ausgewählten Rezepte
if selected_recipes:
    download_multiple_recipes(recipe_folder, selected_recipes)























