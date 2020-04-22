import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import LinearNDInterpolator


data = pd.read_excel('dane_wyjsciowe/PKT.xlsx', 'Sheet1' )

X = np.array(data['X'].to_list())
Y = np.array(data['Y'].to_list())
H = np.array(data['H_ort'].to_list())

A = np.array([X,Y])
print(A)
oczko = 1

x_min = int(np.min(X))
y_min = int(np.min(Y))
x_max = x_min+50#int(np.max(X))+1
y_max = y_min+50#int(np.max(Y))+1
wx = np.arange(x_min, x_max, oczko)
wy = np.arange(y_min, y_max, oczko)



