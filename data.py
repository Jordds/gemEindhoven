import streamlit as st
import pandas as pd
import numpy as np

sorama = pd.read_csv('https://raw.githubusercontent.com/Jordds/gemEindhoven/main/sorama.csv',  nrows = 5)
vinotion = pd.read_csv('https://raw.githubusercontent.com/Jordds/gemEindhoven/main/csv_vinotion_sept.csv', nrows = 5)
tno = pd.read_csv('https://raw.githubusercontent.com/Jordds/gemEindhoven/main/csv_dust_sept.csv', nrows = 5)

devID = sorama['deviceId']
s = sorama['content'].str.split(',', n=3, expand = True)
s = s.rename(columns={0: 'measurementType', 1 :'timestamp', 2:'duration', 3:'value'})
s['timestamp'] = s['timestamp'].str[10:29]
s['date'] = pd.to_datetime(s['timestamp']).dt.date
s['time'] = pd.to_datetime(s['timestamp']).dt.time
s['hour'] = pd.to_datetime(s['timestamp']).dt.hour
s['value'] = s['value'].str.extract('(\d*\.\d+|\d+)', expand = False).astype(float)
s['measurementType'] = s['measurementType'].str[21:25]
s = s[['date', 'time', 'hour','measurementType', 'value']]
df3 = pd.concat([s, devID], axis=1)
df3['value'] = df3['value'].astype('float16') #reducing load on RAM




vinotion['Date'] = pd.to_datetime(vinotion['timestamp']).dt.date
vinotion['Time'] = pd.to_datetime(vinotion['timestamp']).dt.time
vinotion['camID'] = vinotion['cameraId'].str[17:19]
vinotion['direction'] = vinotion['ruleId'].str[20:27].str.replace('/', ' ')
vinotion['speed'] = vinotion['speed'] * 3.6 #csv contains m/s not km/h
df2 = vinotion[['Date', 'Time', 'speed', 'classification', 'camID','direction']]

conditions = [
        (df2['camID'] == '12') & (df2['direction'] == 'Count 0'),
        (df2['camID'] == '12') & (df2['direction'] == 'Count 1'),
        (df2['camID'] == '12') & (df2['direction'] == 'Count 2'),
        (df2['camID'] == '11') & (df2['direction'] == 'Count 0'),
        (df2['camID'] == '11') & (df2['direction'] == 'Count 1'),
        (df2['camID'] == '13') & (df2['direction'] == 'Count 0'),
        (df2['camID'] == '15') & (df2['direction'] == 'Count 0'),
        (df2['camID'] == '15') & (df2['direction'] == 'Count 1'),
        (df2['camID'] == '15') & (df2['direction'] == 'Count 2'),
        (df2['camID'] == '15') & (df2['direction'] == 'Count 3'),
        (df2['camID'] == '14') & (df2['direction'] == 'Count 0'),
        (df2['camID'] == '14') & (df2['direction'] == 'Count 1'),
        (df2['camID'] == '14') & (df2['direction'] == 'Count 2')
    ]
values = ['Onze Lieve Vrouwestraat',
          'Crossover from city',
          'Crossover to city',
          'From Kennedylaan',
          'Ring',
          'Ring',
          'From City', 
          'From Ring', 
          'Crossover to left',
          'Crossover to right',
          'Ring',
          'To the city',
          'Illegal turning'
         ]
df2['real_direction'] = np.select(conditions, values)
df2 = df2[['Date', 'Time', 'speed', 'classification', 'camID','real_direction']]

tno = tno.drop(tno.iloc[:,15:23], axis = 1)
tno['Lat'] = tno['geoPointLocation'].str.extract('(\d*\.\d+|\d+)', expand = False).astype(float)
tno['Lon'] = tno['geoPointLocation'].str[15:].str.extract('(\d*\.\d+|\d+)', expand = False).astype(float)
tno['Date'] = pd.to_datetime(tno['timestamp']).dt.date
tno['Time'] = pd.to_datetime(tno['timestamp']).dt.time
df = tno[['Date', 'Time', 'Lat', 'Lon', 'pm1', 'pm10', 'pm25']]


st.title("Data verzameld door de sensoren")
st.subheader("Sorama")
st.write(sorama)
st.write(df3)


st.subheader("vinotion")
st.write(vinotion)
st.write(df2)



st.subheader("TNO")
st.write(tno)
st.write(df)

