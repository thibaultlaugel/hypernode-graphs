# -*- coding: utf-8 -*-
import numpy as np, pandas

############ Final prediction
#  This script aims at predicting the outcomes of the testing set games, and compute the prediction accuracy
# 
# Process:
#    1. import train and test datasets and rosters, as well as predicted skills
#    2. fill unkown players with average skill
#    3. add up team skills
#    4. compare to winning teams for test games
#    5. compute accuracy
#################################################################################



#import df_test, test_rosters, train_rosters, Yu
Yu = np.genfromtxt (path + 'matrix_skills_pred.csv', delimiter=",")




#skill joined with players
train_rosters['skill'] = Yu




#average predicted skill
s_ = float(sum(Yu)/len(Yu))




# team skill = sum of players skills
test_rost_sk = pandas.merge(test_rosters, train_rosters[['player_id','skill']], how='left', left_on='player_id', right_on='player_id')
test_rost_sk = test_rost_sk.fillna(s_) #if player is unknown : average skill
teams_sk = test_rost_sk[['team_id','skill']].groupby('team_id').sum() #team total skills
teams_sk = teams_sk.reset_index()


#merge of the skills of the winning team
w_sk = pandas.merge(df_test[['wteam','wscore','lteam','lscore']], teams_sk, how='left', left_on='wteam', right_on='team_id')
#merge of the skills of the losing team
all_sk = pandas.merge(w_sk, teams_sk, how='left', left_on='lteam', right_on='team_id')

#if skill of winning team is higher then the prediction was correct
good_pred = all_sk[all_sk['skill_x']>all_sk['skill_y']]
bad_pred = all_sk[all_sk['skill_x']<all_sk['skill_y']]

#accuracy
accuracy = len(good_pred)/len(all_sk)
