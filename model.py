import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

data = pd.read_excel('POSITIONS.xlsx')
data.sort_values(by='Time', inplace=True)
complete_data = data.dropna(subset=['StopLoss', 'TakeProfit'])
incomplete_data = data[data['StopLoss'].isnull() | data['TakeProfit'].isnull()]
X_train = complete_data[['Price', 'Volume']]
y_sl_train = complete_data['StopLoss']
y_tp_train = complete_data['TakeProfit']
knn_sl = KNeighborsRegressor(n_neighbors=3)
knn_tp = KNeighborsRegressor(n_neighbors=3)

knn_sl.fit(X_train, y_sl_train)
knn_tp.fit(X_train, y_tp_train)
X_incomplete = incomplete_data[['Price', 'Volume']]
incomplete_data['StopLoss'] = knn_sl.predict(X_incomplete)
incomplete_data['TakeProfit'] = knn_tp.predict(X_incomplete)
final_data = pd.concat([complete_data, incomplete_data])

#print(final_data)

X = data[['Price', 'StopLoss', 'TakeProfit']]
y_profit = data['Volume'] * (data['TakeProfit'] - data['Price']) - data['Commission'] - data['Swap']
y_loss = data['Volume'] * (data['Price'] - data['StopLoss']) + data['Commission'] + data['Swap']
model_profit = LinearRegression()

imputer = SimpleImputer(strategy='mean')
data[['StopLoss', 'TakeProfit']] = imputer.fit_transform(data[['StopLoss', 'TakeProfit']])
scaler = StandardScaler()
data[['Price', 'StopLoss', 'TakeProfit']] = scaler.fit_transform(data[['Price', 'StopLoss', 'TakeProfit']])
X = data[['Price', 'StopLoss', 'TakeProfit']]
y_profit = data['Volume'] * (data['TakeProfit'] - data['Price']) - data['Commission'] - data['Swap']
y_loss = data['Volume'] * (data['Price'] - data['StopLoss']) + data['Commission'] + data['Swap']

model_profit = LinearRegression()
model_profit.fit(X, y_profit)

model_loss = LinearRegression()
model_loss.fit(X, y_loss)


