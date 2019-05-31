# LINEAR REGRESSION
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


data = pd.read_csv('/Users/user/PycharmProjects/coba/Dataset.csv')
data.dropna(inplace=True)
data['JumlahPenduduk'] = data['JumlahPenduduk'].str.replace(',', '')
data['JumlahPenduduk'] = data['JumlahPenduduk'].astype(float)
data['Kemiskinan'] = data['Kemiskinan'].str.replace(',', '')
data['Kemiskinan'] = data['Kemiskinan'].astype(float)
data['Pendapatan'] = data['Pendapatan'].str.replace(',', '')
data['Pendapatan'] = data['Pendapatan'].astype(float)
data['Golput14'] = data['Golput14'].str.replace(',', '')
data['Golput14'] = data['Golput14'].astype(float)
data['Golput19'] = data['Golput19'].str.replace(',', '')
data['Golput19'] = data['Golput19'].astype(float)
# print(data.head())
# print(data.dtypes)

X = data[['Golput14','Golput19', 'JumlahPenduduk', 'Kemiskinan', 'Pendapatan']]
y = data[['Class']]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
print(len(X_train))

clf = LinearRegression()
# clf.fit(X_train, y_train)
clf.fit(X_train, y_train)
LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
print(clf.predict(X_test))
print(y_test)
print(clf.score(X_test, y_test))

# melihat plot data X dan Y
plt.scatter(data['Class'], data['JumlahPenduduk'], edgecolors='pink')
plt.scatter(data['Class'], data['Kemiskinan'], edgecolors='brown')
plt.scatter(data['Class'], data['Pendapatan'], edgecolors='grey')
plt.scatter(data['Class'], data['Golput14'], edgecolors='yellow')
plt.scatter(data['Class'], data['Golput19'], edgecolors='brown')
plt.title('Grafik data golput, kemiskinan, pendapatan dan jumlah penduduk dibandingkan dengan Class')
plt.show()
