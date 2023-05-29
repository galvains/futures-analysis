import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

from statsmodels.stats.outliers_influence import summary_table
from matplotlib import pyplot as plt


def analysis():
    # чтение данных из csv
    eth_futures = pd.read_csv('/Users/yarik/Desktop/ETHUSDT-1m-2023-04.csv')
    btc_price = pd.read_csv('/Users/yarik/Desktop/BTCUSDT-1m-2023-04.csv')
    df = pd.concat([eth_futures, btc_price], axis=1).dropna()

    # создание массивов данных для вычислений
    x = sm.add_constant(df['28480.07000000'])  # '28480.0700' -> это наименование столбца продажи в csv BTCUSDT
    __x = df['28480.07000000']  # массив BTCUSDT без константы
    y = df['close']  # массив продажи в csv ETHUSDT

    # вычисление корреляции
    correlation = pd.concat([x, y], axis=1).dropna()
    print(correlation.corr())

    # оценка параметров методом наименьших квадратов
    result_linear_ols = sm.OLS(y, x).fit()
    print(result_linear_ols.summary())

    # предварительная визуализация регрессионного анализа
    # axes = sns.jointplot(
    #     x=__x, y=y,
    #     kind='reg',
    #     ci=95)
    # plt.show()


    b0 = result_linear_ols.params['const']
    b1 = result_linear_ols.params['28480.07000000']

    st, data, ss2 = summary_table(result_linear_ols, alpha=0.05)
    st_data_df = pd.DataFrame(st.data)

    st_df = st_data_df.copy()
    # изменим наименования столбцов
    str = st_df.iloc[0, 0:] + ' ' + st_df.iloc[1, 0:]
    st_df = st_df.rename(str, axis='columns')
    # удалим строки 0, 1
    st_df = st_df.drop([0, 1])
    # изменим индекс
    st_df = st_df.set_index(np.arange(0, result_linear_ols.nobs))
    # добавим новый столбец - значения переменной X
    st_df.insert(1, 'BTCUSDT', __x)
    # отсортируем по возрастанию значений переменной X
    st_df = st_df.sort_values(by='BTCUSDT')
    # создание рисунка (Figure) и области рисования (Axes)
    fig, axes = plt.subplots(figsize=(13, 8))

    # заголовок области рисования (Axes)
    title_axes = 'Линейная регрессионная модель'
    axes.set_title(title_axes, fontsize=14)
    
    # фактические данные
    sns.scatterplot(
        x=st_df['BTCUSDT'], y=st_df['Dep Var Population'],
        label='фактические данные',
        s=50,
        color='red',
        ax=axes)
    
    # график регрессионной модели
    label_legend_regr_model = f'линейная регрессия Y = {b0:.3f} + {b1:.4f}*X'
    sns.lineplot(
        x=st_df['BTCUSDT'], y=st_df['Predicted Value'],
        label=label_legend_regr_model,
        color='blue',
        ax=axes)
    
    # доверительный интервал средних значений переменной Y
    Mean_ci_low = st_df['Mean ci 95% low']
    plt.plot(
        st_df['BTCUSDT'], Mean_ci_low,
        color='magenta', linestyle='--', linewidth=1,
        label='доверительный интервал средних значений Y')
    Mean_ci_upp = st_df['Mean ci 95% upp']
    plt.plot(
        st_df['BTCUSDT'], Mean_ci_upp,
        color='magenta', linestyle='--', linewidth=1)
    
    # доверительный интервал индивидуальных значений переменной Y
    Predict_ci_low = st_df['Predict ci 95% low']
    plt.plot(
        st_df['BTCUSDT'], Predict_ci_low,
        color='orange', linestyle='-.', linewidth=2,
        label='доверительный интервал индивидуальных значений Y')
    Predict_ci_upp = st_df['Predict ci 95% upp']
    plt.plot(
        st_df['BTCUSDT'], Predict_ci_upp,
        color='orange', linestyle='-.', linewidth=2)

    axes.legend(prop={'size': 12})
    plt.show()


def main():
    analysis()


if __name__ == '__main__':
    main()
