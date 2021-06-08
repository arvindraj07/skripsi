# -*- coding: utf-8 -*-
"""Skripsi LSTM 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gm1FA-aiiidDYqwUeOeG-uwbmdGoPJmr
"""

import streamlit as st
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
df = pd.read_csv('data-covid-indonesia.csv')
df = df[:304]
# st.write(df)

df = df.set_index('Total Kasus')
# df.head()

print(df.dtypes)

# df.columns

df['Aceh'] = df['Aceh'].str.replace(',', '')
df['Bali'] = df['Bali'].str.replace(',', '')
df['Banten'] = df['Banten'].str.replace(',', '')
df['Babel'] = df['Babel'].str.replace(',', '')
df['Bengkulu'] = df['Bengkulu'].str.replace(',', '')
df['DIY'] = df['DIY'].str.replace(',', '')
df['Jakarta'] = df['Jakarta'].str.replace(',', '')
df['Jambi'] = df['Jambi'].str.replace(',', '')
df['Jabar'] = df['Jabar'].str.replace(',', '')
df['Jateng'] = df['Jateng'].str.replace(',', '')
df['Jatim'] = df['Jatim'].str.replace(',', '')
df['Kalbar'] = df['Kalbar'].str.replace(',', '')
df['Kaltim'] = df['Kaltim'].str.replace(',', '')
df['Kalteng'] = df['Kalteng'].str.replace(',', '')
df['Kalsel'] = df['Kalsel'].str.replace(',', '')
df['Kaltara'] = df['Kaltara'].str.replace(',', '')
df['Kep Riau'] = df['Kep Riau'].str.replace(',', '')
df['NTB'] = df['NTB'].str.replace(',', '')
df['Sumsel'] = df['Sumsel'].str.replace(',', '')
df['Sumbar'] = df['Sumbar'].str.replace(',', '')
df['Sulut'] = df['Sulut'].str.replace(',', '')
df['Maluku'] = df['Maluku'].str.replace(',', '')
df['Papbar'] = df['Papbar'].str.replace(',', '')
df['Papua'] = df['Papua'].str.replace(',', '')
df['Sulbar'] = df['Sulbar'].str.replace(',', '')
df['NTT'] = df['NTT'].str.replace(',', '')
df['Gorontalo'] = df['Gorontalo'].str.replace(',', '')
df['Sumut'] = df['Sumut'].str.replace(',', '')
df['Sultra'] = df['Sultra'].str.replace(',', '')
df['Sulsel'] = df['Sulsel'].str.replace(',', '')
df['Sulteng'] = df['Sulteng'].str.replace(',', '')
df['Lampung'] = df['Lampung'].str.replace(',', '')
df['Riau'] = df['Riau'].str.replace(',', '')
df['Malut'] = df['Malut'].str.replace(',', '')

df = df.apply(pd.to_numeric, errors='coerce')
df.head(2)

df_g = df[['Aceh', 'Bali', 'Banten', 'Babel', 'Bengkulu', 'DIY', 'Jakarta',
           'Jambi', 'Jabar', 'Jateng', 'Jatim', 'Kalbar', 'Kaltim', 'Kalteng',
           'Kalsel', 'Kaltara', 'Kep Riau', 'NTB', 'Sumsel', 'Sumbar', 'Sulut',
           'Sumut', 'Sultra', 'Sulsel', 'Sulteng', 'Lampung', 'Riau', 'Malut',
           'Maluku', 'Papbar', 'Papua', 'Sulbar', 'NTT', 'Gorontalo']]
# df_g.tail()

df_g = df_g.apply(pd.to_numeric, errors='coerce')

df_g['date'] = pd.date_range(start='3/18/2020', end='15/1/2021')
df_g = df_g.set_index('date')
df_g.head()

df_g.to_csv('data-covid-clean.csv')

df_transpose = df_g.T
df_transpose.head()

df_transpose['2021-01-15'].count()

df_transpose.to_csv('data-covid-transpose.csv')

# df_g['Jakarta']


df_j = df_g['Aceh']
difference = df_j.diff().fillna(df_j[0]).astype(np.int64)

print("Difference between rows(Period=1):")

print(difference)


plt.figure(figsize=(20, 5))
difference.plot()
plt.grid(True)
plt.title("Angkat kenaikan kasus per hari di Jakarta")
plt.show()

total_dialy_cases = df_transpose.sum(axis=0).astype(np.int64)
#total_cases = df.sum(axis=0).astype(np.int64)
# total_dialy_cases

plt.figure(figsize=(20, 5))
total_dialy_cases.plot()
plt.grid(True)
plt.title("Total Kasus di Indonesia per hari")
plt.plot()
st.write("")
st.write("Total Kasus di Indonesia per hari")
st.line_chart(total_dialy_cases)


kasus_per_hari = total_dialy_cases.diff().fillna(
    total_dialy_cases[0]).astype(np.int64)
# kasus_per_hari

plt.figure(figsize=(20, 5))
kasus_per_hari.plot()
plt.grid(True)
plt.title("Angka kenaikan Kasus per hari  di Indonesia")
plt.show()

st.write("Angka kenaikan Kasus per hari  di Indonesia")
st.line_chart(kasus_per_hari)

df_j.head()

df_diff = difference[204:304]
# df_diff

# df_transpose.head()

# initialize list of lists
data = df_j.rename(index={'date': ''})

# Create the pandas DataFrame
df1 = pd.DataFrame(data, columns=['Aceh'])

# print dataframe.
# df1

#del df1.index.name

#df_confirmed_country = df_confirmed[df_confirmed["Country/Region"] == country]
#df_confirmed_country = pd.DataFrame(df_confirmed_country[df_confirmed_country.columns[4:]].sum(),columns=["confirmed"])
#df_confirmed_country.index = pd.to_datetime(df_confirmed_country.index,format='%m/%d/%y')

#df_confirmed_country.plot(figsize=(10,5),title="COVID confirmed cases")

# initialize list of lists
#data = df_diff

# Create the pandas DataFrame
#df1 = pd.DataFrame(data, columns = ['Jakarta'])

# print dataframe.
# df1

# Use data until 14 days before as training
x = len(df1)-14

train = df1.iloc[:x]
test = df1.iloc[x:]
test1 = df_j.iloc[x:]

# test

# scale or normalize data as the data is too skewed
scaler = MinMaxScaler()
scaler.fit(train)

train_scaled = scaler.transform(train)
test_scaled = scaler.transform(test)

#scaler = MinMaxScaler(feature_range=(0, 1))
#scaled = scaler.fit_transform(dataset)

# Use TimeSeriestrain_generator to generate data in sequences.
# Alternatively we can create our own sequences.

# Sequence size has an impact on prediction, especially since COVID is unpredictable!
seq_size = 13   # number of steps (lookback)
n_features = 1  # number of features. This dataset is univariate so it is 1
train_generator = TimeseriesGenerator(
    train_scaled, train_scaled, length=seq_size, batch_size=1)
print("Total number of samples in the original training data = ", len(train))  # 271
print("Total number of samples in the generated data = ",
      len(train_generator))  # 264 with seq_size=7

# Check data shape from generator
x, y = train_generator[10]  # Check train_generator
# Takes 7 days as x and 8th day as y (for seq_size=7)

# Also generate test data
test_generator = TimeseriesGenerator(
    test_scaled, test_scaled, length=seq_size, batch_size=1)
print("Total number of samples in the original training data = ",
      len(test))  # 14 as we're using last 14 days for test
print("Total number of samples in the generated data = ", len(test_generator))  # 7
# Check data shape from generator
x, y = test_generator[0]


# Define Model
model = Sequential()
model.add(LSTM(128, activation='relu', return_sequences=True,
               input_shape=(seq_size, n_features)))
model.add(LSTM(32, activation='relu'))
model.add(Dense(64))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

model.summary()
# print('Train...')
##########################

history = model.fit_generator(train_generator,
                              validation_data=test_generator,
                              epochs=100, steps_per_epoch=10)

# plot the training and validation accuracy and loss at each epoch
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# forecast
prediction = []  # Empty list to populate later with predictions

current_batch = train_scaled[-seq_size:]  # Final data points in train
current_batch = current_batch.reshape(1, seq_size, n_features)  # Reshape

# Predict future, beyond test dates
future = 7  # Days
for i in range(len(test) + future):
    current_pred = model.predict(current_batch)[0]
    prediction.append(current_pred)
    current_batch = np.append(current_batch[:, 1:, :], [
                              [current_pred]], axis=1)

# Inverse transform to before scaling so we get actual numbers
rescaled_prediction = scaler.inverse_transform(prediction)

time_series_array = test.index  # Get dates for test data

# Add new dates for the forecast period
for k in range(0, future):
    time_series_array = time_series_array.append(
        time_series_array[-1:] + pd.DateOffset(1))

# Create a dataframe to capture the forecast data
df_forecast = pd.DataFrame(
    columns=["actual_confirmed", "predicted"], index=time_series_array)

df_forecast.loc[:, "predicted"] = rescaled_prediction[:, 0]
df_forecast.loc[:, "actual_confirmed"] = test["Aceh"]

# Plot
st.line_chart(df_forecast)
