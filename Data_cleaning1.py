
# coding: utf-8

# In[26]:

import pandas as pd
import numpy as np


# In[5]:

filepath = '/Users/DanLo1108/Documents/NCAA Tournament Project/Data/'


# In[13]:

#Maps team names from Four Factors and Misc data to summary data

team_map = {'Brigham Young': 'BYU',
            'Nevada Las Vegas': 'UNLV',
            'Virginia Commonwealth': 'VCU',
            'Southern California': 'USC',
            'Louisiana St.': 'LSU',
            'Pennsylvania': 'Penn',
            "St. Mary's": "Saint Mary's",
            'Central Florida': 'UCF',
            'St. Louis': 'Saint Louis',
            'Southern Mississippi': 'Southern Miss',
            'Wisconsin Green Bay': 'Green Bay',
            'NC Greensboro': 'UNC Greensboro',
            'Texas Christian': 'TCU',
            'Southern Methodist': 'SMU',
            'Missouri Kansas City': 'UMKC',
            'Wisconsin Milwaukee': 'Milwaukee',
            'NC Asheville': 'UNC Asheville',
            'NC Greensboro': 'UNC Greensboro',
            'NC Wilmington': 'UNC Wilmington',
            'IUPU Fort Wayne': 'IPFW',
            'Texas Arlington': 'UT Arlington',
            'MD Baltimore County': 'UMBC',
            'Florida International': 'FIU',
            'Long Island': 'LIU Brooklyn',
            'Grambling': 'Grambling St.',
            'Texas San Antonio': 'UTSA',
            "St. Peter's": "Saint Peter's",
            'Texas El Paso': 'UTEP',
            'Virginia Military Inst': 'VMI',
            'NJ Inst of Technology': 'NJIT',
            'South Carolina Upstate': 'USC Upstate'
            }


# In[14]:

for i in range(3,15):
    if i < 10:
        year='0'+str(i)
    else:
        year=str(i)
        
    offense_table_name='offense'+year
    defense_table_name='defense'+year
    misc_table_name='misc'+year
    
    data_off = pd.read_csv(filepath+offense_table_name+'.csv')
    data_def = pd.read_csv(filepath+defense_table_name+'.csv')
    data_misc = pd.read_csv(filepath+misc_table_name+'.csv')
    
    do=data_off
    dd=data_def
    dm=data_misc
    
    for team in team_map:
        if team in set(data_off.TeamName):
            ind=data_off[data_off.TeamName==team].index.values
            data_off.loc[ind,'TeamName']=team_map[team]
        
        if team in set(data_def.TeamName):
            ind=data_def[data_def.TeamName==team].index.values
            data_def.loc[ind,'TeamName']=team_map[team]
            
        if team in set(data_misc.TeamName):
            ind=data_misc[data_misc.TeamName==team].index.values
            data_misc.loc[ind,'TeamName']=team_map[team]
    
    
    data_off.to_csv(filepath+offense_table_name+'.csv',index=False)
    data_def.to_csv(filepath+defense_table_name+'.csv',index=False)
    data_misc.to_csv(filepath+misc_table_name+'.csv',index=False)


# In[96]:

#Maps team names from kenpom data to kaggle data

team_map={'Abilene Christian':'Abilene Chr',
          'Albany':'Albany NY',
          'American':'American Univ',
          'Arkansas Little Rock':'Ark Little Rock',
          'Arkansas Pine Bluff':'Ark Pine Bluff',
          'Bethune Cookman':'Bethune-Cookman',
          'Birmingham Southern':'Birmingham So',
          'Boston University':'Boston Univ',
          'LIU Brooklyn':'Brooklyn',
          'Cal Poly':'Cal Poly SLO',
          'Cal St. Fullerton':'CS Fullerton',
          'Cal St. Bakersfield':'CS Bakersfield',
          'Cal St. Northridge':'CS Northridge',
          'Central Arkansas':'Cent Arkansas',
          'Central Connecticut':'Central Conn',
          'Central Michigan':'C Michigan',
          'Sacramento St':'CS Sacramento',
          'Charleston Southern':'Charleston So',
          'College of Charleston':'Col Charleston',
          'The Citadel':'Citadel',
          'Coastal Carolina':'Coastal Car',
          'East Tennessee St':'ETSU',
          'Eastern Illinois':'E Illinois',
          'Eastern Kentucky':'E Kentucky',
          'Eastern Michigan':'E Michigan',
          'Eastern Washington':'E Washington',
          'FIU':'Florida Intl',
          'Fairleigh Dickinson':'F Dickinson',
          'Florida Atlantic':'FL Atlantic',
          'Florida Gulf Coast':'FL Gulf Coast',
          'George Washington':'G Washington',
          'Georgia Southern':'Ga Southern',
          'Grambling St':'Grambling',
          'Green Bay':'WI Green Bay',
          'Houston Baptist':'Houston Bap',
          'Illinois Chicago':'IL Chicago',
          'Kennesaw St':'Kennesaw',
          'Kent St':'Kent',
          'Louisiana Lafayette':'ULL',
          'Louisiana Monroe':'ULM',
          'Loyola Chicago':'Loyola-Chicago',
          'Loyola Marymount':'Loy Marymount',
          'Maryland Eastern Shore':'MD E Shore',
          'Middle Tennessee':'MTSU',
          'Middle Tennessee St':'MTSU',
          'Milwaukee':'WI Milwaukee',
          'Mississippi Valley St':'MS Valley St',
          'Monmouth':'Monmouth NJ',
          "Mount St. Mary's":"Mt St Mary's",
          'Nebraska Omaha':'NE Omaha',
          'North Carolina A&T':'NC A&T',
          'North Carolina Central':'NC Central',
          'North Carolina St':'NC State',
          'North Dakota St':'N Dakota St',
          'Northern Colorado':'N Colorado',
          'Northern Illinois':'N Illinois',
          'Northern Kentucky':'N Kentucky',
          'Northwestern St':'Northwestern LA',
          'Prairie View A&M':'Prairie View',
          'SIU Edwardsville':'Edwardsville',
          "Saint Joseph's":"St Joseph's PA",
          'Saint Louis':'St Louis',
          "Saint Mary's":"St Mary's CA",
          "Saint Peter's":"St Peter's",
          'South Carolina St':'S Carolina St',
          'South Dakota St':'S Dakota St',
          'Southeast Missouri St':'SE Missouri St',
          'Southeastern Louisiana':'SE Louisiana',
          'Southern':'Southern Univ',
          'Southern Illinois':'S Illinois',
          'Southwest Missouri St':'Missouri St',
          'Southwest Texas St':'Texas St',
          'St. Bonaventure':'St Bonaventure',
          'St. Francis NY':'St Francis NY',
          'St. Francis PA':'St Francis PA',
          "St. John's":"St John's",
          'Stephen F. Austin':'SF Austin',
          'Tennessee Martin':'TN Martin',
          'Texas A&M Corpus Chris':'TAM C. Christi',
          'Texas Pan American':'TX Pan American',
          'Texas Southern':'TX Southern',
          'Troy St':'Troy',
          'UC Santa Barbara':'Santa Barbara',
          'UMKC':'Missouri KC',
          'UMass Lowell':'MA Lowell',
          'USC Upstate':'SC Upstate',
          'UTSA':'UT San Antonio',
          'Utah Valley St':'Utah Valley',
          'VCU':'VA Commonwealth',
          'Western Carolina':'W Carolina',
          'Western Illinois':'W Illinois',
          'Western Kentucky':'W Kentucky',
          'Western Michigan':'W Michigan',
          'Winston Salem St':'W Salem St',
          'Brigham Young': 'BYU',
          'Central Florida': 'UCF',
          'Florida International': 'Florida Intl',
          'Houston BaptiSt': 'Houston Bap',
          'MD Baltimore County':'UMBC',
          'Miami (OH)': 'Miami OH',
          'NC Asheville':'UNC Asheville',
          'NC Greensboro': 'UNC Greensboro',
          'NC Wilmington': 'UNC Wilmington',
          'Pennsylvania': 'Penn',
          'South Carolina Upstate': 'SC Upstate',
          'Southern Methodist': 'SMU',
          'Southern Mississippi': 'Southern Miss',
          "St. Louis": 'St Louis',
          "St. Mary's": "St Mary's CA",
          "St. Peter's": "St Peter's",
          'Texas A&M Corpus Christi': 'TAM C. Christi',
          'Texas Arlington': 'UT Arlington',
          'Texas San Antonio': 'UT San Antonio',
          'Wisconsin Green Bay': 'WI Green Bay',
          'Wisconsin Milwaukee': 'WI Milwaukee'
          }


# In[11]:

kenpom_data=pd.read_csv(filepath+'kenpom_data.csv')


# In[12]:

def remove_periods(x):
    return x.strip('.')

kenpom_data['team_name']=kenpom_data.apply(lambda x: remove_periods(x.team_name), axis=1)


# In[13]:

#kenpom_data=pd.read_csv(filepath+'kenpom_data.csv')

for team in team_map:
    if team in set(kenpom_data.team_name):
        ind=kenpom_data[kenpom_data.team_name==team].index.values
        kenpom_data.loc[ind,'team_name']=team_map[team]
        
kenpom_data.to_csv(filepath+'kenpom_data.csv',index=False)


# In[97]:

#Maps team names of homecourt data to teams data
homecourt=pd.read_csv(filepath+'homecourt.csv')
teams=pd.read_csv(filepath+'teams.csv')


# In[98]:

#Removes periods
def remove_periods(x):
    return x.strip('.')

homecourt['team_name']=homecourt.apply(lambda x: remove_periods(x.team_name), axis=1)


# In[99]:

#Converts bad names to good names
for team in team_map:
    if team in set(homecourt.team_name):
        ind=homecourt[homecourt.team_name==team].index.values
        homecourt.loc[ind,'team_name']=team_map[team]
        
homecourt=homecourt.merge(teams,how='outer',on='team_name')


# In[103]:

homecourt.to_csv(filepath+'homecourt.csv')


# In[ ]:



