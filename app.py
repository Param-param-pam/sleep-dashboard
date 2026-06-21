import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Sleep Dashboard", layout="wide")

# Данные

data = [
    ['09.06','Юля',8.5,8.5],
    ['09.06','Даша',7.5,8],
    ['10.06','Юля',5.5,6],
    ['10.06','Даша',7,7.5],
    ['11.06','Юля',6.7,6.7],
    ['11.06','Даша',6.5,6.8],
    ['12.06','Юля',7.5,7.5],
    ['12.06','Даша',8,8],
    ['13.06','Юля',4,4.5],
    ['13.06','Даша',4,4.5],
    ['14.06','Юля',9,9],
    ['14.06','Даша',8.5,8.5],
    ['15.06','Юля',4.5,4.5],
    ['15.06','Даша',8,7.5],
    ['16.06','Юля',8,8.5],
    ['16.06','Даша',6,6],
    ['17.06','Юля',5.5,5.5],
    ['17.06','Даша',6.5,7],
    ['18.06','Юля',7,7],
    ['18.06','Даша',7,7],
    ['19.06','Юля',2.5,2.5],
    ['19.06','Даша',7,7],
    ['20.06','Юля',9,9],
    ['20.06','Даша',7.5,7.5],
    ['21.06','Юля',7,7],
    ['21.06','Даша',9,9.5]
    ]

df = pd.DataFrame(data, columns=['date','name','min','max'])
df['sleep'] = (df['min']+df['max'])/2
df['date']=pd.to_datetime(df['date'],format = '%d.%m')

st.title("😴 Sleep Dashboard")

# KPI
col1, col2, col3 = st.columns(3)
avg_sleep = df.groupby('name')['sleep'].mean()
std_sleep = df.groupby('name')['sleep'].std()
deficit = df.assign(deficit=df['sleep']-7).groupby('name')['deficit'].sum()

st.metric("Средний сон Юля", f"{avg_sleep['Юля']:.2f}")
st.metric("Средний сон Даша", f"{avg_sleep['Даша']:.2f}")

st.write("___")

# График тренда
st.subheader("📈 Тренд сна")

fig = px.line(df, x='date', y='sleep', color = 'name', markers=True)
fig.add_hline(y=7.4)

st.plotly_chart(fig, width='stretch')

# Календарь сна (heatmap)
st.subheader("🗓️ Календарь сна")

fig2 = px.density_heatmap(df, x = 'date', y ='name', z = 'sleep', color_continuous_scale="RdYlGn")

st.plotly_chart(fig2, width='stretch')

# Сравнение
st.subheader("⚖️ Сравнение")

pivot = df.pivot(index='date', columns='name', values='sleep')
pivot['diff'] = pivot['Юля'] - pivot['Даша']

st.bar_chart(pivot['diff'])

# Прогноз сна
st.subheader("🔮 Прогноз сна")

forecast = []

for name in ['Юля', 'Даша']:
    temp = df[df['name']==name]
    trend = np.polyfit(range(len(temp)), temp['sleep'], 1)[0]
    mean = temp['sleep'].mean()

    for i in range(1, 8):
        forecast.append([i, name, mean + trend * i])

forecast = pd.DataFrame(forecast, columns=['day', 'name', 'sleep'])

fig3 = px.line(forecast, x='day', y='sleep', color='name', markers=True)
fig3.add_hline(y=8)

st.plotly_chart(fig3, width='stretch')

# Таблица
st.subheader("📋 Табличка")
st.dataframe(df)
