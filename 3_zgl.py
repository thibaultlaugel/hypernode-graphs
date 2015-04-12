# -*- coding: utf-8 -*-
import numpy as np
from numpy import linalg


############ ZGL for skill prediction
#  This script aims at using the ZGL algorithm to find a harmonic solution for the skill minimization problem
# 
# Process:
#    1. import matrices W and Laplacian, compute virtual nodes skills
#    2. keep wanted rows
#    3. compute skill predictions
#    4. save the skill vector
#################################################################################






path = 'C:/Users/Thibault/Desktop/MVA/Graph/Project/Material/Tables/'

n = 1740  #nb players
N = 1841 #nb total nodes



L = np.genfromtxt (path + 'matrix_laplacian_reg.csv', delimiter=",")
W = np.genfromtxt (path + 'matrix_weights.csv', delimiter=",")



#virtual nodes skills
Yl = np.transpose(np.matrix(range(0,101))) 



#keep wanted rows and columns
Luu = L[0:n,0:n]
Wul = W[0:n,n:N+1] 



#ZGL
Yu2 = np.dot(linalg.inv(Luu), Wul)
Yu = np.dot(Yu2, Yl)



np.savetxt(path+'matrix_skills_pred.csv', Yu, delimiter=',')
