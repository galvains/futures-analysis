# futures-analysis

Проект для анализа рынка фьючерсов и регрессионного анализа.

### futures_bot
При запуске требует ввести любой фьючерс, который есть на Binance.
Далее происходит анализ его цены в течении последнего часа. Если разница между средним арифметическим этих значений и последним значением изменилась более чем на 1%, произсодит вывод в телеграм-бота о изминении цены.

### regression_analysis
Для запуска требуются csv-файлы с данными двух монет.
Происходит вычисление собственной цены монеты, вычитая корректировки относительно другой монеты (в моем случае btc).

-----

Project for futures market analysis and regression analysis.

### futures_bot
When launched, it requires you to enter any futures, which are available on Binance.
It then analyzes its price for the last hour. If the difference between the arithmetic average of those values and the latest value has changed by more than 1%, it telegrams the bot with the price change.

### regression_analysis
You need csv-files with the data of two coins to run it.
It calculates its own coin price by subtracting corrections relative to the other coin (btc in my case).
