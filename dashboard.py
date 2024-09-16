import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.stats import ttest_ind

st.set_page_config(layout='centered', page_title='Dashboard')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Download data
@st.cache_data
def load_data(filename):
    data = pd.read_csv(filename, sep=",", encoding='windows-1251')
    return data

data_file = st.file_uploader("Upload CSV", type="csv")
if data_file:
    with st.sidebar:
        st.header("Ввод параметров")
        work_days = st.text_input('Количество рабочих дней (work_days)', '2')
        age1 = st.text_input('Возраст (age)', '35')

    work_days = int(work_days)
    era = int(age1)

    st.subheader("Выбранные значения:")
    st.write("Количество рабочих дней:", work_days)
    st.write("Возраст:", era)

    data = load_data(data_file)
    data.columns = ['work_days', 'age', 'sex']

    st.write("* Загруженные данные:")
    st.table(data.head())

    for i in range(len(data['sex'])):
        if data.loc[i, 'sex'] == 'Ж':
            data.loc[i, 'sex'] = 0
        else:
            data.loc[i, 'sex'] = 1
    data['sex'] = data['sex'].astype(str).astype(int)

    st.write("* Описание данных:")
    st.dataframe(data.describe())
    number_data = data.drop('sex', axis=1)

    st.write(f"Дисперсия по рабочим дням: {round(number_data.var()[0], 2)}")
    st.write(f"Дисперсия по возрасту: {round(number_data.var()[1], 2)}")
    st.write(f"Корреляция величин: {round(number_data.corr().iloc[0, 1], 2)}")
    st.write("Уровень значимости: 0.05")

    st.header("Проверка 1 гипотезы: Мужчины пропускают в течение года более "
              f"{work_days} рабочих дней по болезни значимо чаще женщин.")
    st.write("Нулевая гипотеза (H0): Мужчины пропускают в течение года не более 2 рабочих "
             "дней по болезни так же часто или реже, чем женщины.")
    st.write("Альтернативная гипотеза (H1): Мужчины пропускают в течение года более 2 "
             "рабочих дней по болезни значимо чаще, чем женщины.")

    data1 = data[data['work_days'] > work_days]

# График распределения сотрудников по полу
    age_counts = data1["sex"].value_counts()
    fig8 = px.pie(
        age_counts,
        values=age_counts.values,
        names=age_counts.index,
        title='Распределение сотрудников по полу, где "Мужчины" - 1, "Женщины" - 0',
        color=age_counts.index
    )
    st.plotly_chart(fig8, use_container_width=True)

    # Матрица рассеяния
    fig1 = px.scatter_matrix(
        data1,
        dimensions=["work_days", "age"],
        color="sex",
        title='Матрица рассеяния: взаимосвязь пропущенных рабочих дней и возраста по полу'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Гистограмма распределения
    fig3 = px.histogram(
        data1,
        x='work_days',
        color='sex',
        barmode='group',
        text_auto=True,
        title='Гистограмма распределения пропущенных рабочих дней по полу'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Тепловая карта корреляций
    fig4 = px.imshow(
        data1.corr(),
        x=['work_days', 'age', 'sex'],
        y=['work_days', 'age', 'sex'],
        title='Тепловая карта корреляций между пропущенными рабочими днями, возрастом и полом'
    )
    st.plotly_chart(fig4, use_container_width=True)

    # t-тест для сравнения между полами
    men = data1.work_days[data1.sex == 1]
    women = data1.work_days[data1.sex == 0]
    stat, p_value = ttest_ind(men, women)

    st.write(f"p-value={p_value:.5f}")
    st.write(f"t-test: statistic={stat:.4f}")

    if p_value >= 0.05:
        st.write("Нет достаточных оснований для отклонения нулевой гипотезы, "
                "так как p_value больше уровня значимости 0.05")
    else:
        st.write("Есть основания отклонить нулевую гипотезу, "
                "так как p_value меньше уровня значимости 0.05")

    # Проверка 2-ой гипотезы
    st.header(f"Проверка 2-ой гипотезы: Работники старше {era} лет пропускают в течение года более {work_days} рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.")
    st.write(f"Нулевая гипотеза (H0): Работники старше {era} лет пропускают в течение года не более 2 рабочих дней по болезни так же часто или реже, чем работники младше {era+1} лет")
    st.write(f"Альтернативная гипотеза (H1): Работники старше {era} лет пропускают в течение года более 2 рабочих дней по болезни значимо чаще своих более молодых коллег (т.е. тех, кто младше {era+1} лет)")

    # Визуализация распределения пропущенных дней по возрастным группам
    fig5 = px.box(
        data,
        x="age",
        y="work_days",
        color='age',
        title='Визуализация распределения пропущенных дней по возрастным группам'
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Разделение на старших и младших
    old = data1[data1['age'] > era]
    young = data1[data1['age'] <= era]
        
    def categorize_age(age):
        return 'old' if age > era else 'young'

    data1['age_type'] = data1['age'].apply(categorize_age)

    # График распределения сотрудников по возрастным категориям
    age_counts2 = data1["age_type"].value_counts()
    fig6 = px.pie(
        age_counts2,
        values=age_counts2.values,
        names=age_counts2.index,
        title='Распределение сотрудников по возрастным категориям',
        color=age_counts2.index
    )
    st.plotly_chart(fig6, use_container_width=True)

    # Гистограмма распределения пропущенных дней по возрасту категориально
    fig7 = px.histogram(
        data1,
        x='work_days',
        color='age_type',
        title='Распределение пропущенных дней по возрасту категориально'
    )
    st.plotly_chart(fig7, use_container_width=True)

    # t-тест для старших и младших сотрудников
    data_old = data1[data1['age_type'] == 'old']
    data_young = data1[data1['age_type'] == 'young']
    stat, p_value = ttest_ind(data_old.work_days, data_young.work_days)

    st.write(f"t-test: statistic={stat:.4f}, p-value={p_value:.5f}")
    st.write(f"p-value={p_value:.5f}")
    st.write(f"t-test: statistic={stat:.4f}")

    if p_value >= 0.05:
        st.write("Нет достаточных оснований для отклонения нулевой гипотезы, "
                "так как p_value больше уровня значимости 0.05")
    else:
        st.write("Есть основания отклонить нулевую гипотезу, "
                "так как p_value меньше уровня значимости 0.05")

