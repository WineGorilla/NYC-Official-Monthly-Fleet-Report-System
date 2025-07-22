import numpy as np
import pandas as pd
from scripts.constants import No_dict 

def clean_value(x):
    if pd.isna(x):
        return np.nan

    if isinstance(x,str):
        x_clean = x.strip().replace(',','')
        if x_clean.upper() in No_dict:
            return np.nan
        if x_clean.endswith('%'):
            try:
                return float(x_clean.rstrip('%'))
            except ValueError:
                return np.nan
        try:
            return float(x_clean)
        except ValueError:
            return np.nan

    if isinstance(x,(int,float)):
        return float(x)
    return np.nan

def Calculate_Vehicle(df,objective):
    final = [0,0]
    test = df[df['Type'].isin(objective)]
    other = test[(test['Utilization Included in Overall Calculation?'] == 'YES - SEASONALLY') | (test['Utilization Included in Overall Calculation?'] == 'YES')]
    final[0] = round(np.sum(other['WeekdaysUsed']) / np.sum(other['WeekdaysAvailable']),3) * 100
    final[1] = round(np.sum(test['FobbedIn']) / np.sum(test['TotalFobbedTrips']),3) * 100

    return final
