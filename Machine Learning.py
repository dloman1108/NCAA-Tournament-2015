
# coding: utf-8

# In[178]:

import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import log_loss
from collections import Counter


# In[3]:

filepath='/Users/DanLo1108/Documents/Projects/NCAA Tournament Project/Data/'


# In[5]:

training_data = pd.read_csv(filepath + 'final_training_data.csv')
testing_data = pd.read_csv(filepath + 'final_testing_data.csv')


# In[10]:

X_train = training_data.drop('result',axis=1)
y_train = training_data.result

X_test = testing_data.drop(['team_1','team_2'],axis=1)


# In[12]:

#Drop null values from train data
def dropnan(df1, df2,features):
    for feat in features:
        inds=df1[pd.notnull(df1[feat])].index.values
        df1=df1.ix[inds]
        df2=df2.ix[inds]
    return df1,df2

X_train,y_train=dropnan(X_train,y_train,X_train.columns.tolist())
#X_test,y_test=dropnan(X_test,y_test,X_test.columns.tolist())

weights = np.array(X_train.game_weight)
X_train=X_train.drop('game_weight',axis=1)


# In[17]:

matchups=[]
for ind in testing_data.index.values:
    x=testing_data.ix[ind]
    matchups.append((x.team_1,x.team_2))


# In[19]:

matchups


# In[20]:

#Adjusts variables so that they are all between 0 and 1
#i.e. adjusts to per-possession vs per-100-possessions
def adjust_variable(x,feat):
    return x[feat]/100.
    
for col in X_train.columns.tolist():
    if X_train[col].mean() > 1:
        X_train[col] = X_train.apply(lambda x: adjust_variable(x,col), axis=1)

for col in X_test.columns.tolist():
    if X_test[col].mean() > 1:
        X_test[col] = X_test.apply(lambda x: adjust_variable(x,col), axis=1)


# In[22]:

best_features=['team_1_pythag', 'team_2_pythag', 'team_1_AdjOE', 'team_2_AdjOE',
       'team_1_AdjDE', 'team_2_AdjDE', 'team_2_Off_eFG_pct',
       'team_1_Off_OR_pct', 'team_2_Def_eFG_pct', 'team_1_Def_eFG_pct',
       'team_1_Off_eFG_pct', 'team_2_OppFG2Pct', 'team_2_Off_TO_pct',
       'team_1_OppFG2Pct', 'team_2_OppStlRate', 'team_1_Off_TO_pct',
       'team_1_FG2Pct', 'team_2_FG3Pct', 'team_2_Off_OR_pct',
       'team_1_OppFG3Pct', 'team_1_OppStlRate', 'team_2_FTPct',
       'team_2_BlockPct', 'team_2_Def_FT_rate', 'team_1_FTPct',
       'team_1_FG3Pct', 'team_1_BlockPct', 'team_1_Def_OR_pct',
       'team_2_OppFTPct', 'team_1_Def_TO_pct', 'team_2_Def_OR_pct',
       'team_2_OppBlockPct', 'team_1_OppBlockPct', 'team_1_OppFTPct',
       'team_2_OppF3GRate', 'team_2_OppARate', 'team_1_Def_FT_rate',
       'team_1_OppARate', 'team_1_OppF3GRate']


# In[23]:

X_train = X_train[best_features]
X_test = X_test[best_features]


# In[25]:

#Lets try logistic regression
#I found that a bagged logistic regression
#yields the lowest AUC
from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

logreg = BaggingClassifier(LogisticRegression())
logreg.fit(X_train,y_train,sample_weight=weights)

pred_probas=logreg.predict_proba(X_test)
pp_adj=[]

#I've determined that I can minimize my log loss by 
#adjusting each probability prediction 

#for i in range(len(pred_probas)):
#    pp_adj.append((pred_probas[i]**.88)/sum(pred_probas[i]**.88))
    


# In[50]:

predictions1={}
for i in range(len(matchups)):
    predictions1[matchups[i]] = [pred_probas[i][1],pred_probas[i][0]]


# In[51]:

predictions2={}
for i in range(len(matchups)):
    predictions2[matchups[i]] = [pp_adj[i][1],pp_adj[i][0]]


# In[55]:

predictions1[('Hampton','Manhattan')]


# In[160]:

#Returns the predicted probabilities for 2 teams
def get_prediction(team1,team2):
    for p in predictions2:
        if p[0]==team1 and p[1]==team2:
            return predictions2[p]
        if p[1]==team1 and p[0]==team2:
            return [predictions2[p][1],predictions2[p][0]]


# In[158]:

play_in_game_teams=['Dayton','Boise St','North Florida','Robert Morris']


# In[159]:

first_round_teams=['Kentucky','Hampton','Cincinnati','Purdue',
                   'West Virginia','Buffalo','Maryland','Valparaiso',
                   'Butler','Texas','Notre Dame','Northeastern','Wichita St',
                   'Indiana','Kansas','New Mexico St','Wisconsin',
                   'Coastal Car','Oregon','Oklahoma St','Arkansas',
                   'Wofford','North Carolina','Harvard','Xavier',
                   'Mississippi','Baylor','Georgia St','VA Commonwealth',
                   'Ohio St','Arizona','TX Southern','Villanova','Lafayette',
                   'NC State','LSU','Northern Iowa','Wyoming','Louisville',
                   'UC Irvine','Providence','To be determined','Oklahoma','Albany NY',
                   'Michigan St','Georgia','Virginia','Belmont','Duke',
                   'To be determined','San Diego St',"St John's",'Utah',
                   'SF Austin','Georgetown','E Washington','SMU','UCLA',
                   'Iowa St','UAB','Iowa','Davidson','Gonzaga','N Dakota St']


# In[218]:

#Function that divides values in dictionary by a divisor
def get_percent(count,divisor):
    for key in count:
        count[key]=round(count[key]/divisor,4)
        
    return count


# In[207]:

def get_next_round(current_round_teams):
    next_round_teams=[]
    for i in range(0,len(current_round_teams),2):
        team1=current_round_teams[i]
        team2=current_round_teams[i+1]
        thres=get_prediction(team1,team2)[0]
        a=np.random.random()
        if a < thres:
            next_round_teams.append(team1)
        if a > thres:
            next_round_teams.append(team2)
            
    return next_round_teams


# In[ ]:

#Runs 50,000 simulations to find the probability of each
#team making each round

second_round_total=[]
sweet_16_total=[]
elite_8_total=[]
final_4_total=[]
finals_total=[]
winners_total=[]
counter=0.0
for i in range(50000):

    pig_winners=[]
    for i in range(0,len(play_in_game_teams),2):
        team1=play_in_game_teams[i]
        team2=play_in_game_teams[i+1]
        thres=get_prediction(team1,team2)[0]
        a=np.random.random()
        if a < thres:
            pig_winners.append(team1)
        if a > thres:
            pig_winners.append(team2)
  
    first_round_teams=['Kentucky','Hampton','Cincinnati','Purdue',
                       'West Virginia','Buffalo','Maryland','Valparaiso',
                       'Butler','Texas','Notre Dame','Northeastern','Wichita St',
                       'Indiana','Kansas','New Mexico St','Wisconsin',
                       'Coastal Car','Oregon','Oklahoma St','Arkansas',
                       'Wofford','North Carolina','Harvard','Xavier',
                       'Mississippi','Baylor','Georgia St','VA Commonwealth',
                       'Ohio St','Arizona','TX Southern','Villanova','Lafayette',
                       'NC State','LSU','Northern Iowa','Wyoming','Louisville',
                       'UC Irvine','Providence',pig_winners[0],'Oklahoma','Albany NY',
                       'Michigan St','Georgia','Virginia','Belmont','Duke',
                       pig_winners[1],'San Diego St',"St John's",'Utah',
                       'SF Austin','Georgetown','E Washington','SMU','UCLA',
                       'Iowa St','UAB','Iowa','Davidson','Gonzaga','N Dakota St']

    
    second_round_teams=get_next_round(first_round_teams)
    second_round_total+=second_round_teams
    
    sweet_16_teams=get_next_round(second_round_teams)
    sweet_16_total+=sweet_16_teams
    
    elite_8_teams=get_next_round(sweet_16_teams)
    elite_8_total+=elite_8_teams
    
    final_4_teams=get_next_round(elite_8_teams)
    final_4_total+=final_4_teams
    
    finals_teams=get_next_round(final_4_teams)
    finals_total+=finals_teams
    
    winner=get_next_round(finals_teams)
    winners_total+=winner
    
    
    counter+=1
    if np.mod(counter,1000)==0:
        print str(int(counter)),' iterations'
        
        
second_round_probs=get_percent(Counter(second_round_total),counter)
sweet_16_probs=get_percent(Counter(sweet_16_total),counter)
elite_8_probs=get_percent(Counter(elite_8_total),counter)
final_4_probs=get_percent(Counter(final_4_total),counter)
finals_probs=get_percent(Counter(finals_total),counter)
winner_probs=get_percent(Counter(winners_total),counter)


# In[296]:

get_prediction('Virginia','Michigan St')


# In[295]:

sweet_16_probs['New Mexico St']


# In[ ]:



