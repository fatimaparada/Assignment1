#Writing code that implements gradient descent to perform linear regression
#Yeswanth Bogireddy & Fatima Parada-Taboada

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import random
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

#import dataset
dataset = pd.read_csv('https://raw.githubusercontent.com/fatimaparada/Assignment1/master/Copy%20of%20Concrete_Data.csv')

# Plot everything
plt.figure(figsize=(15, 10))
plt.scatter(dataset['Cement (component 1)(kg in a m^3 mixture)'], dataset['Concrete compressive strength(MPa, megapascals) '])

#Splitting data
X_train, X_test, y_train, y_test = train_test_split(dataset['Cement (component 1)(kg in a m^3 mixture)'],
                                                    dataset['Concrete compressive strength(MPa, megapascals) '])
#Plotting training and testing data
plt.figure(figsize=(15, 10))
plt.scatter(X_train, y_train, color = 'blue', label='Training Data')
plt.scatter(X_test, y_test, color = 'red', label='Testing Data')


class GradientDescent:

    def __init__(self, alp, bta, iterations, momentumsInterval): #------------------->Constructor to intialize the values for gradient descent.
        self.alp = alp
        self.bta = bta
        self.iteration_1 = iterations
        self.size = 0
        self.momentum = momentumsInterval
        self.optimalweights = []
        self.optimal_bias = 0

    def calcPredition(self, X_train, coefficients, intercept): #------------------------->Prediction
        predictions = pd.Series()
        predictions = 0
        for i in range(len(coefficients)):
            predictions = coefficients[i] * X_train.values
        predictions += intercept
        return predictions

    def calcLoss(self, X_train, y_train, coefficients, intercept):  #-----------------> MSE
        predictions = self.calcPredition(X_train, coefficients, intercept)
        return ((predictions - y_train) ** 2).sum() * (1 / (2 * self.size))

    def run_gradient_descent(self, X_train, y_train, coefficients, intercept):#-------------------> Preforms momentum gradient decesnt
        i = 0
        while i < self.iteration_1:
            predictions = self.calcPredition(X_train, coefficients, intercept)
            intercept_derivative = (1 / self.size) * (predictions - y_train).sum()
            self.momentum[0] = (self.bta * self.momentum[0]) + ((i - self.bta) * intercept_derivative)
            intercept -= ((self.alp) * self.momentum[0])
            for j in range(len(coefficients)):
                coeff_derivative = (1 / self.size) * ((predictions - y_train) * X_train).sum()
                self.momentum[j + 1] = (self.bta * self.momentum[j + 1]) + ((1 - self.bta) * coeff_derivative)
                coefficients[j] -= (self.alp * self.momentum[j + 1])
            i += 1
        error = self.calcLoss(X_train, y_train, coefficients, intercept)
        return error, coefficients, intercept

    def momentumGradientD(self, X_train, y_train): #----------------> Calling mgd with randomly generated values
        self.size = X_train.shape[0]
        i = 0
        minError = float('inf')
        init_intercept = y_train.values.min()
        iterations = int(y_train.values.max()) - int(y_train.values.min())
        while i < iterations:
            coefficients = []
            coefficients.append(random.uniform(0.0, 8.0)) # change it
            currentError, coefficients, intercept = self.run_gradient_descent(X_train, y_train, coefficients, init_intercept)
            if (currentError < minError):
                minError = currentError
                self.optimalweights = coefficients
                self.optimal_bias = init_intercept
            init_intercept += 0.4
            i += 0.4
            #Print(i,bias/intercept,curr_error,coeff)
        return minError, self.optimalweights, self.optimal_bias

    def predict(self, X_test):
        return self.calcPredition(X_test, self.optimalweights, self.optimal_bias)


alp = 0.00005
bta = 0.9
iterations = 1000
#import dataset
dataset = pd.read_csv('https://raw.githubusercontent.com/fatimaparada/Assignment1/master/Copy%20of%20Concrete_Data.csv')

size = dataset.shape[0]
momentumIterval = [0, 0]

model = GradientDescent(alp, bta, iterations, momentumIterval)
#print(dataset['Concrete compressive strength(MPa, megapascals) '].min())
#print(dataset['Concrete compressive strength(MPa, megapascals) '].max())
print(model.momentumGradientD(dataset['Cement (component 1)(kg in a m^3 mixture)'],
                                                  dataset['Concrete compressive strength(MPa, megapascals) ']))
print((model).optimalweights,(model).optimal_bias)
predictions = model.predict(X_test)

print('Mean squared error: ')
print(mean_squared_error(y_test.values, predictions))

print('R2 scored: ')
print(r2_score(y_test.values, predictions))

plt.figure(figsize=(15,10))
plt.plot(X_test, predictions, color='g', label='Linear Regression')
plt.scatter(X_test, y_test, label='Actual Testing Data')
