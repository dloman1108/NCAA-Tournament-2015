
# coding: utf-8

# In[4]:

import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import log_loss


# In[9]:

filepath='/Users/DanLo1108/Documents/Projects/NCAA Tournament Project/Data/'


# In[10]:

reg_season = pd.read_csv(filepath + 'reg_season_train.csv')
tourney = pd.read_csv(filepath + 'tourney_test.csv')


# In[11]:

X_train = reg_season.drop('result',axis=1)
y_train = reg_season.result

X_test = tourney.drop('result',axis=1)
y_test = tourney.result


# In[12]:

#Drop null values from train and test data
def dropnan(df1, df2,features):
    for feat in features:
        inds=df1[pd.notnull(df1[feat])].index.values
        df1=df1.ix[inds]
        df2=df2.ix[inds]
    return df1,df2

X_train,y_train=dropnan(X_train,y_train,X_train.columns.tolist())
X_test,y_test=dropnan(X_test,y_test,X_test.columns.tolist())

weights = np.array(X_train.game_weight)
X_train=X_train.drop('game_weight',axis=1)


# In[13]:

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

# Find best features from a random forest model
# From previous tests I've determined n_estimators = 40 
# and max_features = sqrt to be the most optimal parameters
#
# **These may be slightly different using my bagged
# logistic regression, but this didn't affect my 
# feature selection

forest = RandomForestClassifier(n_estimators=40,max_features='sqrt')
forest.fit(X_train,y_train,sample_weight=weights)

preds=forest.predict(X_test)
score = forest.score(X_test,y_test)
log_loss = sklearn.metrics.log_loss(y_test, forest.predict_proba(X_test), eps=1e-15, normalize=True)
feat_imps = forest.feature_importances_


# In[24]:

feat_imps_df = pd.DataFrame({'Feature':np.array(X_train.columns.tolist()),
                                                'Importance':feat_imps})

feat_imps_df.sort('Importance',ascending=False)


# In[35]:

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
#adjusting each probability prediction to 
for i in range(len(y_test)):
    pp_adj.append((pred_probas[i]**.88)/sum(pred_probas[i]**.88))
    
log_loss(y_test, pp_adj, eps=1e-15, normalize=True)


# In[709]:

#Feature selection - I iterate through the best features and leave
#one out, and then check the AUC
for feat in best_features:
    #f=[bf for bf in best_features if bf != feat]
    f=best_features
    feats=np.array(features)[f]
    ll=[]
    for j in range(5):
        lr_bagging = BaggingClassifier(LogisticRegression())

        lr_bagging.fit(X_train[feats],y_train,sample_weight=weights)

        pred_probas1=lr_bagging.predict_proba(X_test[feats])
        pp_adj=[]
        for i in range(len(y_test)):
            pp_adj.append((pred_probas1[i]**.88)/sum(pred_probas1[i]**.88))

        ll.append(log_loss(y_test, pp_adj, eps=1e-15, normalize=True))
    print feat, np.mean(ll)


# In[14]:

#Results of feature selection

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


# In[15]:

X_train = X_train[best_features]
X_test = X_test[best_features]


# In[16]:

#Final model - bagged logistic regression
#with reduced features

logreg = BaggingClassifier(LogisticRegression())
logreg.fit(X_train,y_train,sample_weight=weights)

pred_probas=logreg.predict_proba(X_test)
pp_adj=[]

#I've determined that I can minimize my log loss by 
#adjusting each probability prediction to 
for i in range(len(y_test)):
    pp_adj.append((pred_probas[i]**.88)/sum(pred_probas[i]**.88))
    
log_loss(y_test, pp_adj, eps=1e-15, normalize=True)


# In[ ]:

#validation: regularization strength and regularization type
from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
Cs=[.1,.5,1,5,10]
regs=['l1','l2']
#for c in Cs:
for reg in regs:
    #logreg = BaggingClassifier(LogisticRegression(C=c))
    logreg = BaggingClassifier(LogisticRegression(penalty=reg))
    logreg.fit(X_train,y_train,sample_weight=weights)

    pred_probas=logreg.predict_proba(X_test)
    pp_adj=[]

    #I've determined that I can minimize my log loss by 
    #adjusting each probability prediction to 
    for i in range(len(y_test)):
        pp_adj.append((pred_probas[i]**.88)/sum(pred_probas[i]**.88))

    print reg, log_loss(y_test, pp_adj, eps=1e-15, normalize=True)


# In[19]:

lls=[0.586515583419,0.583077107628,0.581886763833,0.583740743521,0.584271049367]


# In[21]:

from pylab import *
plot(Cs,lls)
title('Log loss vs regularization strength (C)',fontsize=20)
xlabel('C',fontsize=16)
ylabel('Log loss',fontsize=16)
show()


# In[ ]:



