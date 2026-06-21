import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Sleep Dashboard", layout="wide")

# Данные

data = [
    ['09.06.2026','Юля',8.5,8.5],
    ['09.06.2026','Даша',7.5,8],
    ['10.06.2026','Юля',5.5,6],
    ['10.06.2026','Даша',7,7.5],
    ['11.06.2026','Юля',6.7,6.7],
    ['11.06.2026','Даша',6.5,6.8],
    ['12.06.2026','Юля',7.5,7.5],
    ['12.06.2026','Даша',8,8],
    ['13.06.2026','Юля',4,4.5],
    ['13.06.2026','Даша',4,4.5],
    ['14.06.2026','Юля',9,9],
    ['14.06.2026','Даша',8.5,8.5],
    ['15.06.2026','Юля',4.5,4.5],
    ['15.06.2026','Даша',8,7.5],
    ['16.06.2026','Юля',8,8.5],
    ['16.06.2026','Даша',6,6],
    ['17.06.2026','Юля',5.5,5.5],
    ['17.06.2026','Даша',6.5,7],
    ['18.06.2026','Юля',7,7],
    ['18.06.2026','Даша',7,7],
    ['19.06.2026','Юля',2.5,2.5],
    ['19.06.2026','Даша',7,7],
    ['20.06.2026','Юля',9,9],
    ['20.06.2026','Даша',7.5,7.5],
    ['21.06.2026','Юля',7,7],
    ['21.06.2026','Даша',9,9.5]
    ]

df = pd.DataFrame(data, columns=['date','name','min','max'])
df['sleep'] = (df['min']+df['max'])/2
df['date']=pd.to_datetime(df['date'],format = '%d.%m.%Y')

st.sidebar.header('Фильтры')
selected_person = st.sidebar.selectbox("Кто", ['Все','Юля','Даша'])

if selected_person =='Все':
    filtered_df = df.copy()
else: filtered_df=df[df['name']== selected_person]

st.title("😴 Sleep Dashboard")

# KPI
col1, col2, col3, col4 = st.columns(4)
avg_sleep = filtered_df['sleep'].mean()
best__sleep = filtered_df['sleep'].max()
worst_sleep = filtered_df['sleep'].min()
#std_sleep = df.groupby('name')['sleep'].std()
#deficit = df.assign(deficit=df['sleep']-7).groupby('name')['deficit'].sum()
sleep_deficit = (filtered_df['sleep'] -7).sum()

#st.metric("Средний сон Юля", f"{avg_sleep['Юля']:.2f}")
#st.metric("Средний сон Даша", f"{avg_sleep['Даша']:.2f}")
with col1:
    st.metric("Средний сон",f"{avg_sleep:.2f} ч")

with col2:
    st.metric("Лучшая ночь",f"{best__sleep:.1f} ч")

with col3:
    st.metric("Худшая ночь",f"{worst_sleep:.1f} ч")

with col4:
    st.metric("Дефицит сна",f"{sleep_deficit:.1f} ч")

st.write("___")

# График тренда
st.subheader("📈 Тренд сна")

fig = px.line(filtered_df, x='date', y='sleep', color = 'name', markers=True)
fig.add_hline(y=7)

st.plotly_chart(fig, width='stretch')

# Календарь сна (heatmap)
st.subheader("🗓️ Календарь сна")

fig2 = px.density_heatmap(filtered_df, x = 'date', y ='name', z = 'sleep', color_continuous_scale="RdYlGn")

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
fig3.add_hline(y=7)

st.plotly_chart(fig3, width='stretch')

# Таблица
st.subheader("📋 Табличка")
st.dataframe(filtered_df)
