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
    ['21.06.2026','Даша',9,9.5],
    ['22.06.2026','Юля',8.5,8.5],
    ['22.06.2026','Даша',7,7],
    ['23.06.2026','Юля',5.5,5.5],
    ['23.06.2026','Даша',7.5,8],
    ['24.06.2026','Юля',6,6],
    ['24.06.2026','Даша',6,6],
    ['25.06.2026','Юля',8,8],
    ['25.06.2026','Даша',7,7],
    ['26.06.2026','Юля',7,7.5],
    ['26.06.2026','Даша',7.5,8],
    ['27.06.2026','Юля',5.5,5.5],
    ['27.06.2026','Даша',8,8],
    ['28.06.2026','Юля',6,6],
    ['28.06.2026','Даша',8,8.5],
    ['29.06.2026','Юля',7,7],
    ['29.06.2026','Даша',7,7.5],
    ['30.06.2026','Юля',5,5],
    ['30.06.2026','Даша',4.5,4.5],
    ['01.07.2026','Юля',4,4],
    ['01.07.2026','Даша',6.5,6.5],
    ['02.07.2026','Юля',4,4],
    ['02.07.2026','Даша',4,4],
    ['03.07.2026','Юля',4.5,4.5],
    ['03.07.2026','Даша',6,6],
    ['04.07.2026','Юля',8,8],
    ['04.07.2026','Даша',7,7.5],
    ['05.07.2026','Юля',4,4],
    ['05.07.2026','Даша',5,5],
    ['06.07.2026','Юля',8,8],
    ['06.07.2026','Даша',8,8.5],
    ['07.07.2026','Юля',6,6],
    ['07.07.2026','Даша',6.5,7],
    ['08.07.2026','Юля',5,5],
    ['08.07.2026','Даша',5.5,5.5],
    ['09.07.2026','Юля',5.5,5.5],
    ['09.07.2026','Даша',6,6],
    ['10.07.2026','Юля',3.5,3.5],
    ['10.07.2026','Даша',7,7],
    ['11.07.2026','Юля',3.5,3.5],
    ['11.07.2026','Даша',5,5],
    ['12.07.2026','Юля',4.5,5],
    ['12.07.2026','Даша',4.5,5],
    ['13.07.2026','Юля',7,7],
    ['13.07.2026','Даша',7,7],
    ['14.07.2026','Юля',6,6],
    ['14.07.2026','Даша',6,6],
    ['15.07.2026','Юля',5,5],
    ['15.07.2026','Даша',5,5],
    ['16.07.2026','Юля',4,4],
    ['16.07.2026','Даша',4.5,4.5],
    ['17.07.2026','Юля',5,5.5],
    ['17.07.2026','Даша',7,7],
    ['18.07.2026','Юля',6,6],
    ['18.07.2026','Даша',6,6],
    ['19.07.2026','Юля',5,5],
    ['19.07.2026','Даша',5,5],
    ['20.07.2026','Юля',6.5,6.5],
    ['20.07.2026','Даша',7,7]
    ]

df = pd.DataFrame(data, columns=['date','name','min','max'])
df['sleep'] = (df['min']+df['max'])/2
df['date']=pd.to_datetime(df['date'],format = '%d.%m.%Y')

st.sidebar.header('⚙️ Фильтры')
selected_person = st.sidebar.selectbox("Кто", ['Все','Юля','Даша'])
selected_period = st.sidebar.radio("📅 Период",[
    "Все время",
    "Последние 7 дней",
    "Последние 14 дней",
    "Последние 30 дней",
    "Свой период"
])

if selected_person =='Все':
    filtered_df = df.copy()
else: filtered_df=df[df['name']== selected_person]

last_date = filtered_df['date'].max()

if selected_period == "Последние 7 дней":
    filtered_df=filtered_df[filtered_df['date'] >last_date - pd.Timedelta(days = 6)]
elif selected_period == "Последние 14 дней":
    filtered_df=filtered_df[filtered_df['date'] >=last_date - pd.Timedelta(days = 13)]
elif selected_period == "Последние 30 дней":
    filtered_df=filtered_df[filtered_df['date'] >=last_date - pd.Timedelta(days = 29)]
elif selected_period == "Свой период":
    #start_day, end_date = st.sidebar.date_input(
    data_range = st.sidebar.date_input(
        "Выбирай период",
        value =(filtered_df['date'].min(), filtered_df['date'].max()))
    
    if len(data_range) == 2:
        start_day, end_date = data_range

    filtered_df = filtered_df[
        (filtered_df['date']>=pd.to_datetime(start_day)) &
        (filtered_df['date']<=pd.to_datetime(end_date))
    ]

st.title("😴 Sleep Dashboard")
st.caption("🌙 Сон - это важно")

# INFO
col7, col8,col9 = st.columns(3)
with col7: st.info(f"Данные с **{df['date'].min().strftime('%d.%m')}**"
                    f"по **{df['date'].max().strftime('%d.%m')}**")
    
with col8: st.info(f"Всего записей **{len(df)}**")

with col9: st.info(f"Последняя запись **{df['date'].max().strftime('%d.%m')}**")

# KPI
col1, col2, col3, col4, col5, col6 = st.columns(6)
avg_sleep = filtered_df['sleep'].mean()
best__sleep = filtered_df['sleep'].max()
worst_sleep = filtered_df['sleep'].min()
sleep_deficit = (filtered_df['sleep'] -7.5).sum()
best ='19.07.2026'

#Sleep_score = 100
avg_deficit = abs(filtered_df['sleep']-7.5).mean()
sleep_variability = filtered_df['sleep'].std()
sleep_score = (100 - avg_deficit*12 - sleep_variability*5 )

sleep_score = max(0, min(100, sleep_score))

with col1:
    st.metric("💤 Средний сон",f"{avg_sleep:.2f} ч")

with col2:
    st.metric("💫 Лучшая ночь",f"{best__sleep:.1f} ч")

with col3:
    st.metric("😵 Худшая ночь",f"{worst_sleep:.1f} ч")

with col4:
    st.metric("🥱 Дефицит сна",f"{sleep_deficit:.1f} ч")

with col4:
    st.metric("✳ Качество сна",f"{sleep_score:.0f}/100")

with col6:
    st.metric("💝 Самая лучшая ночь ",f"{best}")

st.write("___")

# График тренда
st.subheader("📈 Тренд сна")

fig = px.line(filtered_df, x='date', y='sleep', color = 'name', markers=True)
fig.add_hline(y=7.5)

st.plotly_chart(fig, width='stretch')

# Календарь сна (heatmap)
#st.subheader("🗓️ Календарь сна")

#fig2 = px.density_heatmap(filtered_df, x = 'date', y ='name', z = 'sleep', color_continuous_scale="RdYlGn")

#st.plotly_chart(fig2, width='stretch')

# Дневник сна
st.subheader("🗓️ Дневник сна")

calendar_df = filtered_df.copy()
calendar_df['quality'] = calendar_df['sleep'].apply(
    lambda x:
    "Хорошо" if x >= 7.5
    else "Нормально" if x >= 6
    else"Недосып"
)

fig_calendar = px.scatter(
    calendar_df,
    x ='date',
    y = 'name',
    color = 'quality',
    color_discrete_map = {"Недосып":"red", "Нормально":"gold", "Хорошо":"green"},
    size='sleep',
    hover_data = ['sleep'])

st.plotly_chart(fig_calendar, width='stretch')

# тепловая карта
st.subheader("🌡️ Тепловая карта сна")

heatmap_df=filtered_df.pivot_table(
    index='name',
    columns='date',
    values='sleep'
)

fig_heatmap = px.imshow(heatmap_df, aspect='auto', color_continuous_scale="RdYlGn")

st.plotly_chart(fig_heatmap, width='stretch')

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
fig3.add_hline(y=7.5)

st.plotly_chart(fig3, width='stretch')

# Таблица
st.subheader("📋 Табличка")
st.dataframe(filtered_df)
