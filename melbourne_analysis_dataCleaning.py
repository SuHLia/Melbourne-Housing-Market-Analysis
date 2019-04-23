#import
import pandas as pd
import numpy as np 
df = pd.read_csv('Melbourne_housing_FULL.csv')
df.head()
#drop columns
#to_drop = ['Postcode','Lattitude','Longtitude']  
#df.drop(to_drop, inplace=True, axis = 1)      
#df.head()

#delete empty Price
df['Price'].replace('', np.nan, inplace = True)
df.dropna(subset=['Price'], inplace = True)

#delete empty Bedroom2
df['Bedroom2'].replace('', np.nan, inplace = True)
df.dropna(subset=['Bedroom2'], inplace = True)
#delete empty & 0 value Bathroom 
df['Bathroom'].replace('', np.nan, inplace = True)
df['Bathroom'].replace(0, np.nan, inplace = True)
df.dropna(subset=['Bathroom'], inplace = True)
#delete empty Car
df['Car'].replace('', np.nan, inplace = True)
df.dropna(subset=['Car'], inplace = True)
#delete empty YearBuilt
df['YearBuilt'].replace('', np.nan, inplace = True)
df.dropna(subset=['YearBuilt'], inplace = True)
#delete empty LandSize & Building Area 
df['Landsize'].replace('', np.nan, inplace = True)
df.dropna(subset=['Landsize'], inplace = True)

df['BuildingArea'].replace('', np.nan, inplace = True)
df.dropna(subset=['BuildingArea'], inplace = True)
#filter LandSize & BuildingArea
dfLandSize = df[df['Landsize'] > 100]  
dfBuildingArea = dfLandSize[dfLandSize['BuildingArea']>50]

#create new column: PriceRange, Method2, Quarter, YearSold, Month, HouseAge
#dfBuildingArea.insert(4,"PriceRange","")
#idx = 0
#new_col = ''
#df.insert(loc=idx, column = 'Test', value = new_col)


dfBuildingArea.insert(loc= 4, column = 'PriceRange', value = '')
dfBuildingArea.insert(loc= 7, column = 'MethodGroup', value = '')
dfBuildingArea.insert(loc= 10, column = 'Quarter', value = '')
dfBuildingArea.insert(loc= 11, column = 'YearSold', value = '')
dfBuildingArea.insert(loc= 12, column = 'Month', value = '')
dfBuildingArea.insert(loc= 13, column = 'HouseAge', value = '')
dfBuildingArea.insert(loc= 14, column = 'AgeGroup', value = '')
dfBuildingArea.insert(loc= 16, column = 'DistanceGroup', value = '')
dfBuildingArea.insert(loc= 19, column = 'BedroomGroup', value = '')
dfBuildingArea.insert(loc= 21, column = 'BathroomGroup', value = '')
dfBuildingArea.insert(loc= 23, column = 'CarGroup', value = '')
dfBuildingArea.insert(loc= 25, column = 'LandSizeGroup', value = '')

#dfBuildingArea['PriceRange'] = ''
#dfBuildingArea['MethodGroup'] = ''
#dfBuildingArea['Quarter'] = ''
#dfBuildingArea['YearSold'] = ''
#dfBuildingArea['Month'] = ''
#dfBuildingArea['HouseAge'] = ''
#dfBuildingArea['AgeGroup'] = ''
#dfBuildingArea['DistanceGroup'] = ''
#dfBuildingArea['BedroomGroup'] = ''
#dfBuildingArea['LandSizeGroup'] = ''
#dfBuildingArea['BathroomGroup'] = ''
#dfBuildingArea['CarGroup'] = ''


#convert date to Month and YearSold
import time
import calendar
dfBuildingArea['YearSold'] = pd.DatetimeIndex(dfBuildingArea['Date']).year
dfBuildingArea['Month'] = pd.DatetimeIndex(dfBuildingArea['Date']).month

#Calculate HouseAge
dfBuildingArea['HouseAge'] =  dfBuildingArea['YearSold'] - dfBuildingArea['YearBuilt']

#filter House Age for less than 200 years old and more than & equal 0
dfHouseAge = dfBuildingArea[dfBuildingArea['HouseAge'] < 200]
dfHouseAge2 = dfHouseAge[dfHouseAge['HouseAge'] >= 0]
df = dfHouseAge2
#Fill up Price Range
def set_pricerange(df):
    if (df['Price'] > 100000) and (df['Price'] <= 700000):
        return 'Low'
    elif (df['Price'] > 700000) and (df['Price'] <= 1200000):
        return 'Medium'
    elif (df['Price'] > 1200000) and (df['Price'] <= 2000000):
        return 'High'
    elif (df['Price'] > 2000000) and (df['Price'] <= 9000000):
        return 'Luxury'

df['PriceRange'] = df.apply(set_pricerange, axis = 1)

#Fill up MethodGroup
def set_methodGroup(df):
    if (df['Method'] == 'S') or (df['Method'] == 'SP') or (df['Method'] == 'VB') or (df['Method'] == 'SA')  or (df['Method'] == 'SS'):
        return 'S'
    elif (df['Method'] == 'PN') or (df['Method'] == 'SN'):
        return 'SP'
    elif (df['Method'] == 'PI') or (df['Method'] == 'N/A'):
        return 'UN'
    elif (df['Method'] == 'NB') or (df['Method'] == 'W'):
        return 'NS'
    
df['MethodGroup'] = df.apply(set_methodGroup, axis = 1)

#Fill up Quarter
def set_Quarter(df):
    if (df['Month'] < 4):
        return 1
    elif (df['Month'] >= 4) and (df['Month'] < 7):
        return 2
    elif (df['Month'] >= 7) and (df['Month'] < 10):
        return 3
    elif (df['Month'] >= 10):
        return 4


df['Quarter'] = df.apply(set_Quarter, axis = 1)

#Fill up AgeGroup
def set_ageGroup(df):
    if (df['HouseAge'] < 30):
        return '<30'
    elif (df['HouseAge'] >= 30) and (df['HouseAge'] < 60):
        return '[30,60)'
    elif (df['HouseAge'] >= 60) and (df['HouseAge'] < 100):
        return '[60,100)'
    elif (df['HouseAge'] >= 100) and (df['HouseAge'] < 200):
        return '[100,200)'

df['AgeGroup'] = df.apply(set_ageGroup, axis = 1)

#Fill up BedroomGroup
def set_BedroomGroup(df):
    if (df['Bedroom2'] < 3):
        return '<3'
    elif (df['Bedroom2'] >= 3) and (df['Bedroom2'] < 5):
        return '[3-4]'
    elif (df['Bedroom2'] >= 5) and (df['Bedroom2'] < 20):
        return '>=5'

df['BedroomGroup'] = df.apply(set_BedroomGroup, axis = 1)

#Fill up BathroomGroup
def set_BathroomGroup(df):
    if (df['Bathroom'] > 0) and (df['Bathroom'] < 3):
        return '[1-2]'
    elif (df['Bathroom'] >= 3) and (df['Bathroom'] < 6):
        return '[3-5]'
    elif (df['Bathroom'] >= 6) and (df['Bathroom'] < 10):
        return '[6-9]'

df['BathroomGroup'] = df.apply(set_BathroomGroup, axis = 1)

#Fill up CarGroup
def set_CarGroup(df):
    if (df['Car'] == 0):
        return '0'
    elif (df['Car'] >= 1) and (df['Car'] < 3):
        return '[1-2]'
    elif (df['Car'] >= 3) and (df['Car'] < 5):
        return '[3-4]'
    elif (df['Car'] >= 5) and (df['Car'] <= 10):
        return '>=5'

df['CarGroup'] = df.apply(set_CarGroup, axis = 1)

#Fill up DistanceGroup
def set_DistanceGroup(df):
    if (df['Distance'] < 7):
        return '[0,7)'
    elif (df['Distance'] >= 7) and (df['Distance'] < 14):
        return '[7,14)'
    elif (df['Distance'] >= 14) and (df['Distance'] < 20):
        return '[14,20)'
    elif (df['Distance'] >= 20) and (df['Distance'] < 49):
        return '>=20'

df['DistanceGroup'] = df.apply(set_DistanceGroup, axis = 1)

##############################################

#size of dataframe 
dfBuildingArea.head()
df.shape

#extract data to csv file
df.to_csv('test1.csv', index = True, header = True)

#function to read front & back data 
def front(self, n):
    return self.iloc[:,:n]

def back(self, n):
    return self.iloc[:, -n:]
pd.DataFrame.front = front
pd.DataFrame.back = back
dfBuildingArea.front(24)
