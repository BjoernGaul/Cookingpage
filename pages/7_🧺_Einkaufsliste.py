import streamlit as st

# Beispiel-Nutzung:
file_path = "./Einkaufsliste.txt"

st.header('🧺 Einkaufsliste')


col1, col2 = st.columns(2)
einkaufslststr = ''

if 'einkaufslst' in st.session_state:
 einkaufslst = st.session_state.einkaufslst
 for zutat in einkaufslst:
  with col1:
   st.button(str(einkaufslst[zutat]) + zutat)
  with col2:
   if st.button('Entfernen', key=zutat):
    st.session_state.einkaufslst.pop(zutat)
    st.rerun()
 for key, value in einkaufslst.items():
  einkaufslststr += f'{value} {key.strip(" ")}\n'


 st.download_button('Download Einkaufsliste', einkaufslststr)






