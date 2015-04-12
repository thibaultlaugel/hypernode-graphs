# -*- coding: utf-8 -*-


import numpy as np, pandas, math
from scipy import linalg


############ Regularized Laplacian Computation
#  This script aims at building the regularized laplacian matrix
# 
# Process:
#    1. import train_rosters and df_train
#    2. compute mu/n
#    3. compute G, B, Gmu, Lmu
#    4. compute D, W
#    4. Save matrices W and Lmu
#################################################################################



p = len(df_train) #number of games in the tournament
n = len(train_rosters) #number of players in the tournament
t = 1 #nb lazy nodes
l = range(100) 
o = 100 #nb outcome nodes
N = n + t + o #total number of nodes



#average number of games for mu/n
aw = df_train[['wteam', 'season']].groupby(['wteam']).count()
al = df_train[['lteam','season']].groupby(['lteam']).count()
atot = aw+al
#1455: 33
som = sum(atot['season'][atot['season']>0]) + 33
moyenne = som/len(atot['season'])
mu_n = moyenne





#need: train_rosters, df_train





print(str(p) + ' games in train set')
print(str(n) + ' players in train set')
print(str(N) + ' total nodes in hypergraph')




############



#Building gradient matrix G
#1 if team won the game, -1 if team lost
G = np.zeros(shape=(p,N))
for j in range(p):
    wteam = int(df_train['wteam'].iloc[[j]])
    lteam = int(df_train['lteam'].iloc[[j]])
    wt_rost = train_rosters['player_id'][train_rosters['team_id']==wteam]
    lt_rost = train_rosters['player_id'][train_rosters['team_id']==lteam]

    #filling corresponding columns for winning and losing teams
    for i in wt_rost:
        ix = int(train_rosters[train_rosters['player_id']==i].index)
        G[j,ix] = 1
    for i in lt_rost:
        ix = int(train_rosters[train_rosters['player_id']==i].index)
        G[j,ix] = -1
    #lazy node = wins every game
    G[j,n] = 1
    #outcome nodes: depending on the score difference, loses every game
    diff_score = df_train['wscore'].iloc[[j]] - df_train['lscore'].iloc[[j]]
    ix_sc = list(l).index(int(diff_score)) -1 #+ 1
    G[j,n+ix_sc] = -1



#building B
B = np.zeros(shape=(n,N+1))
for i in range(n):
    B[i,i] = -1
    B[i,N] = 1

    
#regularized gradient
m = np.zeros(shape=(p, 1))
Gm = np.c_[G,m]
Gmu = np.r_[Gm, math.sqrt(mu_n)*B]


#regularized laplacian
Deltamu = np.dot(np.transpose(Gmu) , Gmu)








#Degree matrix: for each node, number of games = sums of abs(rows) for each col of G
deg = sum(abs(G))
D = np.diag(deg)

#Laplacian
L = np.dot(np.transpose(G),G)


#Weiht matrix
W = D - L




path = 'C:/Users/Thibault/Desktop/MVA/Graph/Project/Material/Tables/' # a changer
np.savetxt(path+'matrix_Laplacian_reg.csv', Deltamu, delimiter=',')
np.savetxt(path+'matrix_weights.csv', W, delimiter=',')
