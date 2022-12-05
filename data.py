import streamlit
import pandas as pd

sorama = pd.read_csv('https://raw.githubusercontent.com/Jordds/gemEindhoven/main/csv_dust_sept.csv', sep = ';', nrows = 5)
vinotion = pd.read_csv('csv_vinotion_sept.csv', nrows = 5)
tno = pd.read_csv('csv_dust_sept.csv', nrows = 5)

st.title("Data verzameld door de sensoren")
st.subtitle("Sorama")
st.write(sorama)

st.subtitle("Vinotion")
st.write(vinotion)

st.subtitle("TNO")
st.write(tno)


