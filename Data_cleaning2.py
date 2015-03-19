
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from pylab import *


# In[2]:

filepath='/Users/DanLo1108/Documents/NCAA Tournament Project/Data/'


# In[3]:

#Reads in regular season results (train), tournament results (test)
#and kenpom data (supplemental)

kenpom_data=pd.read_csv(filepath+'kenpom_data.csv')
reg_season=pd.read_csv(filepath+'regular_season_compact_results.csv')
tourney=pd.read_csv(filepath+'tourney_compact_results.csv')
teams=pd.read_csv(filepath+'teams.csv')


# In[4]:

#Only considers regular season games played after 2002
#and the 2011-2014 NCAA Tournaments:

reg_season=reg_season[reg_season.season >= 2003]
tourney=tourney[tourney.season >= 2003]


# In[5]:

#Ratio of tournament games to season games
tourney_ratio=float(len(tourney))/len(reg_season)


# In[45]:

reg_season['tourney_game']=np.array([0.0]*len(reg_season))
tourney['tourney_game']=np.array([1.0]*len(tourney))


# In[46]:

#Moves earlier tourneys from tourney data to regular season data
#I'm sticking with 'reg_season' and 'tourney' as general train/test names

reg_season=reg_season.append(tourney[tourney.season < 2011])
tourney=tourney[tourney.season >= 2011]


# In[47]:

#Join kenpom data and teams

#kenpom_data=kenpom_data.merge(teams,how='left',on='team_name')


# In[6]:

#Adjust for homecourt advantage:
homecourt=pd.read_csv(filepath+'homecourt.csv')
def get_adj_gamescore_winner(x,homecourt): 
    points = x.wscore
    if x.wloc == 'N':
        return points
    if x.wloc == 'H':
        team=x.wteam
        point_diff=float(homecourt[homecourt.team_id == team]['point_diff'])
        return points-point_diff/2.
    if x.wloc == 'A':
        team=x.lteam
        point_diff=float(homecourt[homecourt.team_id == team]['point_diff'])
        return points+point_diff/2.
    
    
def get_adj_gamescore_loser(x,homecourt):
    points = x.lscore
    if x.wloc == 'N':
        return points
    if x.wloc == 'H':
        team=x.wteam
        point_diff=float(homecourt[homecourt.team_id == team]['point_diff'])
        return points+point_diff/2.
    if x.wloc == 'A':
        team=x.wteam
        point_diff=float(homecourt[homecourt.team_id == team]['point_diff'])
        return points-point_diff/2.
        
reg_season['wscore']=reg_season.apply(lambda x: get_adj_gamescore_winner(x,homecourt),axis=1)
reg_season['lscore']=reg_season.apply(lambda x: get_adj_gamescore_loser(x,homecourt),axis=1)


# In[49]:

#Gets the pythagorean win percentage of the winning team 
#and associated weight:

def pythagorean(w_score,l_score):
    return w_score**13.91/(w_score**13.91+l_score**13.91)

def get_pythag(x):
    if x.numot == 0:
        return pythagorean(x.wscore,x.lscore)
    else:
        return .50
    
def get_gamescore_weight(x):
    pyth = get_pythag(x)
    return 1/(1-(pyth-.5))


#I want to make regular season and tournament games weighted 50/50,
#so I use the tourney_ratio to weigh tourney games

def get_tourney_weight(x,ratio):
    if x.tourney_game==1:
        return 1./ratio
    if x.tourney_game==0:
        return 1
        


#Gets weight associated with the day the game was played on:
def get_day_weight(x):
    day=x.daynum
    return (float(day)/132)**4/2+1

#Gets total weight based on day weight and game score weight:
def get_total_weight(x,tourney_ratio):
    day_weight=get_day_weight(x)
    score_weight=get_gamescore_weight(x)
    tourney_weight=get_tourney_weight(x,tourney_ratio)
    
    return day_weight*score_weight*tourney_weight
    
    
reg_season['game_weight']=reg_season.apply(lambda x: get_total_weight(x,tourney_ratio),axis=1)


# In[10]:

pyth=1
#1/(1-(pyth-.5))
1/(1.5-pyth)


# In[50]:

#Randomly assign teams as team_1 and team_2, and set
#result=1 if team_1 was the winner
import random
def assign_teams(df):
    team_1=[]
    team_2=[]
    result=[]
    for ind in df.index.values:
        d=df.ix[ind]
        a=random.random()
        if a < .5:
            team_1.append(d.wteam)
            team_2.append(d.lteam)
            result.append(1)
        else:
            team_1.append(d.lteam)
            team_2.append(d.wteam)
            result.append(0)
    df['team_1'] = np.array(team_1)
    df['team_2'] = np.array(team_2)
    df['result'] = np.array(result)


# In[51]:

assign_teams(reg_season)
reg_season = reg_season.drop(['daynum','wteam','wscore','lteam','lscore','numot','tourney_game'],axis=1)


# In[52]:

assign_teams(tourney)
tourney = tourney.drop(['daynum','wteam','wscore','lteam','lscore','numot','tourney_game'],axis=1)


# In[53]:

#Gets features from kenpom_data
kenpom_data.columns.tolist()
not_features=['season','team_name','team_id']
features=[col for col in kenpom_data.columns.tolist() if col not in not_features]


# In[54]:

def get_feature(x,team_num,feat,data):
    team=x[team_num]
    seas=x.season
    if len(data[data.team_id==team][data.season==seas][feat] > 0):
        return float(data[data.team_id==team][data.season==seas][feat])
    else:
        return np.nan


# In[55]:

#*** THIS TAKES A LONG TIME

#Get features for team 1 in regular season 
for feat in features:
    col_name='team_1_'+feat
    reg_season[col_name]=reg_season.apply(lambda x: get_feature(x,'team_1',feat,kenpom_data),axis=1)
    print col_name
    
#Get features for team 2 in regular season
for feat in features:
    col_name='team_2_'+feat
    reg_season[col_name]=reg_season.apply(lambda x: get_feature(x,'team_2',feat,kenpom_data),axis=1)
    print col_name


# In[56]:

#***THIS ALSO TAKES A LONG TIME

#Get features for team 1 in tourney
for feat in features:
    col_name='team_1_'+feat
    tourney[col_name]=tourney.apply(lambda x: get_feature(x,'team_1',feat,kenpom_data),axis=1)
    print col_name
    
#Get features for team 2 in tourney
for feat in features:
    col_name='team_2_'+feat
    tourney[col_name]=tourney.apply(lambda x: get_feature(x,'team_2',feat,kenpom_data),axis=1)
    print col_name


# In[59]:

#Drops unneeded columns from reg_season and saves to .csv
r=reg_season.drop(['season','wloc','team_1','team_2','team_1_Unnamed: 0','team_2_Unnamed: 0'],axis=1)
r.to_csv(filepath+'reg_season_train.csv',index=False)


# In[58]:

#Drops unneeded columns from tourney and saves to .csv
t=tourney.drop(['season','wloc','team_1','team_2','team_1_Unnamed: 0','team_2_Unnamed: 0'],axis=1)
t.to_csv(filepath+'tourney_test.csv',index=False)


# In[ ]:



