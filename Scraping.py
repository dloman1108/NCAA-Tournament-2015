
# coding: utf-8

# In[253]:

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib2
import re


# In[254]:

url='http://www.predictionmachine.com/college-basketball-homecourt-advantage'
filepath='/Users/DanLo1108/Documents/NCAA Tournament Project/Data/'


# In[7]:

#Gets contents of url web page
request=urllib2.Request(url)
page = urllib2.urlopen(request)


# In[9]:

#Reads contents of page
content=page.read()
soup=BeautifulSoup(content,'lxml')


# In[18]:

#Finds results of table
results=soup.find_all({'table':'standard sortable'})


# In[247]:

#Puts results of table into arrays teams and points
results=soup('table')[1].find_all('td')
teams=[]
points=[]
i=0
for r in results:
    for item in r:
        if np.mod(i,3) == 1:
            teams.append(item.strip('\r\n\t\t\t\t'))
        if np.mod(i,3) == 2:
            points.append(item.strip('\r\n\t\t\t\t'))
            
        i+=1
            
teams=np.array(teams)
points=np.array(points)


# In[248]:

#Changes type and format of points
def get_points(x):
    if '(' in x:
        points=re.sub('\(','-',x)
        points=re.sub('\)','',points)
        return float(points)
    else:
        points=x
        return float(points)
    
points = np.array(map(lambda x: get_points(x), points))


# In[250]:

#Saves to pandas dataframe
homecourt=pd.DataFrame({'team_name':teams,'point_diff':points})


# In[255]:

homecourt.to_csv(filepath+'homecourt.csv',index=False)


# In[ ]:



