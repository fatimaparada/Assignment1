#Assignment1 Part 2
#Use an ML Library that performs linear regression from SciKit Learn
#Yeswanth Bogireddy & Fatima Parada-Taboada

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score

#------------------------------------> import data
datafile = pd.read_csv('https://raw.githubusercontent.com/fatimaparada/Assignment1/master/Copy%20of%20Concrete_Data.csv')

#------------------------------------> plot independent and dependent variable from dataset
plt.figure(figsize=(15,10))
plt.scatter(datafile['Cement (component 1)(kg in a m^3 mixture)'],
                                                    datafile['Concrete compressive strength(MPa, megapascals) '])
#-----------------------------------> Split datset into training and testing
X_train, X_test, y_train, y_test = train_test_split(datafile['Cement (component 1)(kg in a m^3 mixture)'],
                                                    datafile['Concrete compressive strength(MPa, megapascals) '])
#-----------------------------------> plot training dataset vs testing dataset
plt.figure(figsize=(15,10))
plt.scatter(X_train, y_train, color = 'blue', label='Training Data')
plt.scatter(X_test, y_test, color = 'red', label='Testing Data')


#-----------------------------------> train values using training dataset and sklearn linear regression 
model = LinearRegression()
bestfit = model.fit(X_train.values.reshape(-1,1),y_train)

#----------------------------------------> finding the prediction line using testing dataset
prediction = model.predict(X_test.values.reshape(-1,1))
print(prediction)

#---------------------------------------> plot prediction line vs testing dataset
plt.figure(figsize=(15,10))
plt.plot(X_test, prediction, color='g', label='Linear Regression')
plt.scatter(X_test, y_test, color= 'purple', label='Actual Test Data')

#weight
print(bestfit.coef_)
#y-intercept
print(bestfit.intercept_)
#mean square error
print(mean_squared_error(y_test.values, prediction))
#r squared 
print(r2_score(prediction, y_test.values))

