
# coding: utf-8

# In[1]:

import mysql.connector
import numpy as np


# In[2]:

filepath='/Users/DanLo1108/Documents/NCAA Tournament Project/Data/'


# In[5]:

cnx = mysql.connector.connect(user='root', database='NCAA_Tourney_final')
cursor = cnx.cursor()


# In[8]:

#Kenpom summary data from 2003 to 2014

for i in range(3,15):
    if i < 10:
        year='0'+str(i)
    else:
        year=str(i)
    table_name='summary'+year
    
    create_table = ('create table ' + table_name + ' '
                    '(TeamName char(25), '
                    'Tempo float, '
                    'RankTempo bigint, '
                    'AdjTempo float, '
                    'RankAdjTempo bigint, '
                    'OE float, '
                    'RankOE bigint, '
                    'AdjOE float, '
                    'RankAdjOE bigint, '
                    'DE float, '
                    'RankDE bigint, '
                    'AdjDE float, '
                    'RankAdjDE bigint, '
                    'Pythag float, '
                    'RankPythag bigint);')
                    
    load_data = ('load data infile "' + filepath + table_name + '_pt.csv" '
                 'into table summary'+year+' FIELDS TERMINATED BY "," IGNORE 1 LINES;')
   
    cursor.execute(create_table)
    cursor.execute(load_data)
    
    add_year = "alter table " + table_name + " add year bigint first;"
    no_safe = "SET SQL_SAFE_UPDATES = 0;"
    set_year = "update " + table_name + " set year=20" + year + ";"
    
    cursor.execute(add_year)
    cursor.execute(no_safe)
    cursor.execute(set_year)
    
    print year


# In[28]:

# Offensive and defense Four Factors:

for i in range(3,15):
    if i < 10:
        year='0'+str(i)
    else:
        year=str(i)
        
    offense_table_name='offense'+year
    defense_table_name='defense'+year

    create_table_offense = ('create table ' + offense_table_name + ' '
                            '(TeamName char(25), '
                            'off_eFG_Pct float, '
                            'off_RankeFG_Pct bigint, '
                            'off_TO_Pct float, '
                            'off_RankTO_Pct bigint, '
                            'off_OR_Pct float, '
                            'off_RankOR_Pct bigint, '
                            'off_FT_Rate float, '
                            'off_RankFT_Rate bigint);')
    
    create_table_defense = ('create table ' + defense_table_name + ' '
                            '(TeamName char(25), '
                            'def_eFG_Pct float, '
                            'def_RankeFG_Pct bigint, '
                            'def_TO_Pct float, '
                            'def_RankTO_Pct bigint, '
                            'def_OR_Pct float, '
                            'def_RankOR_Pct bigint, '
                            'def_FT_Rate float, '
                            'def_RankFT_Rate bigint);')
                            
    
    load_table_offense = ('load data infile "' + filepath + offense_table_name + '.csv" '
                          'into table ' + offense_table_name + ' FIELDS TERMINATED BY "," IGNORE 1 LINES;')
    
    load_table_defense = ('load data infile "' + filepath + defense_table_name + '.csv" '
                          'into table ' + defense_table_name + ' FIELDS TERMINATED BY "," IGNORE 1 LINES;')
    
    
    cursor.execute(create_table_offense)
    cursor.execute(load_table_offense)
    
    cursor.execute(create_table_defense)
    cursor.execute(load_table_defense)
    
    print year
    
    


# In[26]:

#Kenpom miscellaneous data from 2003 to 2014

for i in range(3,15):
    if i < 10:
        year='0'+str(i)
    else:
        year=str(i)
    table_name='misc'+year
    
    create_table1 = ('create table ' + table_name + ' '
                    '(TeamName char(25), '
                    'FG2Pct float, '
                    'RankFG2Pct bigint, '
                    'FG3Pct float, '
                    'RankFG3Pct bigint, '
                    'FTPct float, '
                    'RankFTPct bigint, '
                    'BlockPct float, '
                    'RankBlockPct bigint, '
                    'OppFG2Pct float, '
                    'RankOppFG2Pct bigint, '
                    'OppFG3Pct float, '
                    'RankOppFG3Pct bigint, '
                    'OppFTPct float, '
                    'RankOppFTPct bigint, '
                    'OppBlockPct float, '
                    'RankOppBockPct bigint, '
                    'F3GRate float, '
                    'RankF3GRate bigint, '
                    'OppF3GRate float, '
                    'RankOppF3GRate bigint, '
                    'ARate float, '
                    'RankARate bigint, '
                    'OppARate float, '
                    'RankOppARate bigint, '
                    'StlRate float, '
                    'RankStlRate bigint, '
                    'OppStlRate float, '
                    'RankOppStlRate bigint, '
                    'DefensiveFingerprint float);')
    
    create_table2 = ('create table ' + table_name + ' '
                    '(TeamName char(25), '
                    'FG2Pct float, '
                    'RankFG2Pct bigint, '
                    'FG3Pct float, '
                    'RankFG3Pct bigint, '
                    'FTPct float, '
                    'RankFTPct bigint, '
                    'BlockPct float, '
                    'RankBlockPct bigint, '
                    'OppFG2Pct float, '
                    'RankOppFG2Pct bigint, '
                    'OppFG3Pct float, '
                    'RankOppFG3Pct bigint, '
                    'OppFTPct float, '
                    'RankOppFTPct bigint, '
                    'OppBlockPct float, '
                    'RankOppBockPct bigint, '
                    'F3GRate float, '
                    'RankF3GRate bigint, '
                    'OppF3GRate float, '
                    'RankOppF3GRate bigint, '
                    'ARate float, '
                    'RankARate bigint, '
                    'OppARate float, '
                    'RankOppARate bigint, '
                    'StlRate float, '
                    'RankStlRate bigint, '
                    'OppStlRate float, '
                    'RankOppStlRate bigint);')
                    
    load_data = ('load data infile "' + filepath + table_name + '.csv" '
                 'into table misc'+year+' FIELDS TERMINATED BY "," IGNORE 1 LINES;')
   
    if i > 3 and i < 8:
        cursor.execute(create_table2)
    if i==3 or i >= 8:
        cursor.execute(create_table1)
        
    cursor.execute(load_data)
    
    print year


# In[31]:

# Joining 4 tables and getting columns that I want:

for i in range(3,15):
    if i < 10:
        year='0'+str(i)
    else:
        year=str(i)
        
    t1='summary'+year
    t2='offense'+year
    t3='defense'+year
    t4='misc'+year
    new_table = 'stats'+year
    
    join_tables = ('create table ' + new_table + ''
                   ' as '
                   'select year, ' + t1 + '.TeamName, AdjTempo, AdjOE, AdjDE, pythag, '
                   'Off_eFG_pct, Off_TO_pct, Off_OR_pct, Off_FT_rate, '
                   'Def_eFG_pct, Def_TO_pct, Def_OR_pct, Def_FT_rate, '
                   'FG2Pct, FG3Pct, F3GRate, FTPct, ARate, BlockPct, StlRate, '
                   'OppFG2Pct, OppFG3Pct, OppF3GRate, OppFTPct, OppARate, OppBlockPct, OppStlRate '
                   'from ' + t1 + ' '
                   'left join ' + t2 + ' on ' + t1 + '.TeamName=' + t2 + '.TeamName '
                   'left join ' + t3 + ' on ' + t1 + '.TeamName=' + t3 + '.TeamName '
                   'left join ' + t4 + ' on ' + t1 + '.TeamName=' + t4 + '.TeamName;')
    
    cursor.execute(join_tables)
    print year

    


# In[32]:

# Combine all years data

combine_tables = ('create table kenpom_data as '
                  'select * from stats03 union '
                  'select * from stats04 union '
                  'select * from stats05 union '
                  'select * from stats06 union '
                  'select * from stats07 union '
                  'select * from stats08 union '
                  'select * from stats09 union '
                  'select * from stats10 union '
                  'select * from stats11 union '
                  'select * from stats12 union '
                  'select * from stats13 union '
                  'select * from stats14;')

cursor.execute(combine_tables)


# In[34]:

#Save to .csv

to_csv = ("select 'year','TeamName','AdjTempo','AdjOE', "
          "'AdjDE','pythag','Off_eFG_pct','Off_TO_pct','Off_OR_pct',"
          "'Off_FT_rate','Def_eFG_pct','Def_TO_pct','Def_OR_pct','Def_FT_rate', "
          "'FG2Pct', 'FG3Pct', 'F3GRate', 'FTPct', 'ARate', 'BlockPct', 'StlRate', "
          "'OppFG2Pct', 'OppFG3Pct', 'OppF3GRate', 'OppFTPct', 'OppARate', 'OppBlockPct', 'OppStlRate' "
          "from kenpom_data "
          "union "
          "select * from kenpom_data "
          "into outfile '" + filepath + "kenpom_data.csv' "
          "fields terminated by ',';")

cursor.execute(to_csv)


# In[27]:

to_csv


# In[ ]:



