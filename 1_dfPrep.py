# -*- coding: utf-8 -*-
import os, pandas, numpy as np



############ Dataframes manipulation
#  This script aims at cleaning scraped data and preparing it for the model
# 
# Process:
#    1. cleaning empty rows
#    2. creating player index
#    3. keeping 5 players per team
#    4. saving new dataframes
#################################################################################


path = 'C:/Users/Thibault/Desktop/MVA/Graph/Project/Material/Tables/' # a changer

#######TODO
# 5




#db teams
df_dic = pandas.read_csv(path + 'teams_dic.csv', sep=';', header = None) #matching team names
#df_2012 = pandas.read_csv(path + 'rosters_scraped_2012.txt', sep = ',', header = None )
df_2013 = pandas.read_csv(path + 'rosters_scraped_2013.csv', sep = ';', header = None )
df_2014 = pandas.read_csv(path + 'rosters_scraped_2014.txt', sep = ',', header = None )
df_teams = pandas.read_csv(path + 'teams.csv', sep = ',' )

#db train test
df_train = pandas.read_csv(path + 'regular_season_compact_results.csv', sep = ',' )
df_test = pandas.read_csv(path + 'regular_season_compact_results_2015.csv', sep = ',' )

#missing rows
#df_2012 = df_2012[df_2012[1] > 0]
df_2013 = df_2013[df_2013[1] > 0]
df_2014 = df_2014[df_2014[1] > 0]

#buggy columns in df_dic
df_dic = df_dic[[1,2]]

#name columns
#df_2012.columns = ['team', 'season', 'firstname', 'name']
df_2013.columns = ['team', 'season', 'firstname', 'name']
df_2014.columns = ['team', 'season', 'firstname', 'name']
df_dic.columns = ['university', 'team']


#missing scraped roster
df_dic = df_dic.dropna()







#Replacing players names, firstname by ids
#df_tot = df_2012.append(df_2013).append(df_2014)
df_tot = df_2013.append(df_2014)
l = df_tot['firstname'] + ' ' + df_tot['name']
l = pandas.Series(l.unique())
ix = pandas.Series(range(1, len(l)+1))
df_playersid = pandas.concat([ix,l], axis = 1)
df_playersid.columns = ['player_id', 'nom']





#adding player id and dropping old names
#df_2012['nom complet'] = df_2012['firstname'] + ' ' + df_2012['name']
#df_2012 = pandas.merge(df_2012, df_playersid, how = 'left', left_on = 'nom complet', right_on = 'nom')
#df_2012 = df_2012[['team', 'season','player_id']]
df_2013['nom complet'] = df_2013['firstname'] + ' ' + df_2013['name']
df_2013 = pandas.merge(df_2013, df_playersid, how = 'left', left_on = 'nom complet', right_on = 'nom')
df_2013 = df_2013[['team', 'season','player_id']]
df_2014['nom complet'] = df_2014['firstname'] + ' ' + df_2014['name']
df_2014 = pandas.merge(df_2014, df_playersid, how = 'left', left_on = 'nom complet', right_on = 'nom')
df_2014 = df_2014[['team', 'season','player_id']]





#traiing dataset definition
df_train = df_train[df_train['season'] >= 2014] #2013




#join roster train db
#df_train_rosters = df_2012.append(df_2013)
df_train_rosters = df_2013





#final rosters tables: 
a = pandas.merge(df_2014, df_dic, how = 'inner', left_on = 'team', right_on = 'team')
b = pandas.merge(a, df_teams, how = 'left', left_on = 'university', right_on = 'team_name')
test_rosters = b[['team_id', 'season', 'player_id']]
test_rosters = test_rosters.drop_duplicates('player_id')

a2 = pandas.merge(df_train_rosters, df_dic, how = 'inner', left_on = 'team', right_on = 'team')
b2 = pandas.merge(a2, df_teams, how = 'left', left_on = 'university', right_on = 'team_name')
train_rosters = b2[['team_id', 'season', 'player_id']]
train_rosters = train_rosters.drop_duplicates('player_id')







#keep first 5 players for each team
train_rosters = train_rosters.groupby('team_id').head(5).reset_index(drop=True)
test_rosters = test_rosters.groupby('team_id').head(5).reset_index(drop=True)






#save dataframes
train_rosters.to_csv(path + 'train_rosters.csv', sep=',')
test_rosters.to_csv(path + 'test_rosters.csv', sep=',')
df_train.to_csv(path + 'df_train.csv', sep=',')
df_test.to_csv(path + 'df_test.csv', sep=',')




