import numpy as np
import random as rand

X_max = 10000
X_min = 2500
Y_min = 0.6
Y_max = 1.8
X = np.random.uniform(0,1,1000)
Z = np.random.uniform(0,1,1000)
pir = np.random.uniform(0.6,0.97,1000)

Y = pir* X + np.sqrt(1-pir**2)*Z

X_new = (X-X.min())/(X.max()-X.min())
Y_new = (Y-Y.min())/(Y.max()-Y.min())
    
X_last = X_new * (X_max-X_min)+X_min

Y_last = Y_new * (Y_max-Y_min)+Y_min

X_mid = X_last.sum()/len(X_last)
Y_mid = Y_last.sum()/len(Y_last)

n = len(X_last)
sum1 = 0.0
sum2 = 0.0
sum3 = 0.0
for i in range(n):
    sum1 += (X_last[i] - X_mid) * (Y_last[i] - Y_mid)
    sum2 += (X_last[i] - X_mid)**2
    sum3 += (Y_last[i] - Y_mid)**2

P_cor = sum1/(np.sqrt(sum2) * np.sqrt(sum3))


print(X_last)
print(Y_last)
print(pir)
print(P_cor)






