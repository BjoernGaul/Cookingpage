import streamlit as st
from fpdf import FPDF
from datetime import date
from streamlit_lottie import st_lottie
from pages.Functions.functions import load_lottiefile

pdf = FPDF()
today = date.today()

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

 pdf.add_page()
 pdf.set_font('Arial', size=20)
 pdf.cell(200,10, txt=f'Einkaufsliste {today}', ln=2, align= 'C')
 pdf.set_font('Arial', size=15)
 pdf.ln(3)
 for key, value in einkaufslst.items():
  pdf.cell(200, 10, txt=f'{value} {key.strip(" ")}\n', ln=1, align='C')
 lis = pdf.output('Einkaufsliste.pdf',dest='S').encode('latin-1')
 st.download_button('Download', lis,file_name='Einkaufsliste.pdf', mime='application/octet-stream')


lottie_coding = load_lottiefile("./Vögel.json")
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
