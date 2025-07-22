import pandas as pd
from scripts.constants import *
import numpy as np
from scripts.utils import Calculate_Vehicle

def divisionCalculate(df):
    test = df[(df['Utilization Included in Overall Calculation?'] == 'YES - SEASONALLY') | (df['Utilization Included in Overall Calculation?'] == 'YES')]
    
    Total_OOS = round(np.sum(test['DaysOOS']) / np.sum(test['DaysOwned']),3) 
    Total_7DayUtilization = round(np.sum(test['DaysUsed']) / np.sum(test['DaysAvailable']),3) 
    Total_WeekdayUtilization = round(np.sum(test['WeekdaysUsed']) / np.sum(test['WeekdaysAvailable']),3) 
    Total_MilesDriven = round(np.sum(test['TotalMiles']))
    Total_FobbedIn = round(np.sum(test['FobbedIn']) / np.sum(test['TotalFobbedTrips']),3) 

    analysis_table = test.groupby('Division/Boro').agg({'DaysOOS':'sum','DaysOwned':'sum','DaysUsed':'sum','DaysAvailable':'sum','WeekdaysUsed':'sum','WeekdaysAvailable':'sum','FobbedIn':'sum','TotalFobbedTrips':'sum','TotalMiles':'sum'})
    analysis_table['OOS Rate'] = round(analysis_table['DaysOOS'] / analysis_table['DaysOwned'],3) 
    analysis_table['Utilization Rate'] = round(analysis_table['DaysUsed'] / analysis_table['DaysAvailable'],3) 
    analysis_table['Weekday Utilization Rate'] = round(analysis_table['WeekdaysUsed'] / analysis_table['WeekdaysAvailable'],3) 
    analysis_table['Fobbed In %'] = round(analysis_table['FobbedIn'] / analysis_table['TotalFobbedTrips'],3) 
    analysis_table['TotalMiles'] = round(analysis_table['TotalMiles'])

    analysis_tem_table = analysis_table[['OOS Rate','Utilization Rate','Weekday Utilization Rate','TotalMiles','Fobbed In %']]
    final_table = pd.DataFrame()

    for i in analysis_tem_table.index:
        if Division_dict.get(i):
            new_index = Division_dict.get(i)
            new_row = pd.DataFrame({
                'OOS Rate':analysis_tem_table.loc[i,'OOS Rate'],
                '7-Day Utilization':analysis_tem_table.loc[i,'Utilization Rate'],
                'Weekday Utilization':analysis_tem_table.loc[i,'Weekday Utilization Rate'],
                'Total Miles Driven':analysis_tem_table.loc[i,'TotalMiles'],
                'Fobbed-In Percentage':analysis_tem_table.loc[i,'Fobbed In %']
            },index=[new_index])
            final_table = pd.concat([final_table,new_row])
    
    return final_table, Total_OOS, Total_7DayUtilization, Total_WeekdayUtilization, Total_MilesDriven, Total_FobbedIn

def vehicleCalculate(df):
    test = df[df['Type'] == 'PICKUP']
    BK = [0,0]
    BX = [0,0]
    MN = [0,0]
    QN = [0,0]
    SI = [0,0]

    other = test[(test['Utilization Included in Overall Calculation?'] == 'YES - SEASONALLY') | (test['Utilization Included in Overall Calculation?'] == 'YES')]
    other_table = other.groupby('Division/Boro').agg({'WeekdaysUsed':'sum','WeekdaysAvailable':'sum'}) 
    other_table['Weekday Utilization Rate'] = round(other_table['WeekdaysUsed'] / other_table['WeekdaysAvailable'],3) 
    
    analysis_table = test.groupby('Division/Boro').agg({'DaysOOS':'sum','DaysOwned':'sum','DaysUsed':'sum','DaysAvailable':'sum','WeekdaysUsed':'sum','WeekdaysAvailable':'sum','FobbedIn':'sum','TotalFobbedTrips':'sum','TotalMiles':'sum'})
    analysis_table['OOS Rate'] = round(analysis_table['DaysOOS'] / analysis_table['DaysOwned'],3) 
    analysis_table['Utilization Rate'] = round(analysis_table['DaysUsed'] / analysis_table['DaysAvailable'],3) 
    analysis_table['Weekday Utilization Rate'] = round(analysis_table['WeekdaysUsed'] / analysis_table['WeekdaysAvailable'],3) 
    analysis_table['Fobbed In %'] = round(analysis_table['FobbedIn'] / analysis_table['TotalFobbedTrips'],3) 
    analysis_table['TotalMiles'] = round(analysis_table['TotalMiles'])    
    
    Total_Group = pd.DataFrame()
    Total_Group['Weekday Utilization Rate'] = other_table['Weekday Utilization Rate']
    Total_Group['Fobbed In %'] = analysis_table['Fobbed In %']

    for i in Total_Group.index:
        if i == "DPAR-BROOKLYN":
            BK[0] += Total_Group.loc[i][0] * 100
            BK[1] += Total_Group.loc[i][1] * 100

        elif i == "DPAR-BRONX":
            BX[0] += Total_Group.loc[i][0] * 100
            BX[1] += Total_Group.loc[i][1] * 100

        elif i == "DPAR-MANHATTAN":
            MN[0] += Total_Group.loc[i][0] * 100
            MN[1] += Total_Group.loc[i][1] * 100

        elif i == "DPAR-QUEENS":
            QN[0] += Total_Group.loc[i][0] * 100
            QN[1] += Total_Group.loc[i][1] * 100

        elif i == "DPAR-STATEN ISLAND":
            SI[0] += Total_Group.loc[i][0] * 100
            SI[1] += Total_Group.loc[i][1] * 100

    final_result_Division_vehicle = pd.DataFrame({
        'BX':BX,
        'BK':BK,
        'MN':MN,
        'QN':QN,
        'SI':SI
    },index=['Weekday Utilization Rate','Fobbed In %']).T

    packers_sum = Calculate_Vehicle(df,packer_features)
    sedans_sum = Calculate_Vehicle(df,sedans_features)
    suvs_sum = Calculate_Vehicle(df,suvs_features)
    vans_sum = Calculate_Vehicle(df,vans_features)

    final_result_vehicle = pd.DataFrame({
        'Packers':packers_sum,
        'Sedans':sedans_sum,
        'SUVs':suvs_sum,
        'Vans':vans_sum
    },index=['Weekday Utilization Rate','Fobbed In %']).T

    return final_result_Division_vehicle, final_result_vehicle
