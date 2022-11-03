# CAMELS-GB-2-HBV-Light
#
# Input projects for HBV-Light (Seibert and Vis 2012) for the 671 GB catchments in the CAMELS-GB dataset (Coxon et al 2020). For each catchment, the dataset has been spl;it into calibration and validation time periods on a 50:50 basis.
# In the src folder, there is the python script that was used for the processing.
#
# Sim Reaney, Durham Univsity
# simreaney.github.io
# November 2022


import pandas as pd
import numpy as np
from pathlib import Path
import os

def main():

    list = open('gaugeList.csv')
    #Skip header
    list.readline()
    for line in list.readlines():

        line = line.split(',')
        print(line)
        fn = 'CAMELS_GB_hydromet_timeseries_' + line[0] + '_19701001-20150930.csv'
        # print(fn)
        df = pd.read_csv(fn, na_values=['?'])
        #fill in missing values with padding. Not great but makes things work
        df = df.fillna(method="pad")
        #if there are values at the start of the series that are 'na', drop these rows
        df = df.dropna()

        df0, df1 = np.array_split(df, 2)

        createHBVLightDataSet(df0, fn, 'cali', line[1])
        createHBVLightDataSet(df1, fn, 'vali', line[1])


def createHBVLightDataSet(df, fn, type, name):
    fnElements = fn.split('_')
    gauge = fnElements[4]
    print(gauge)
    name = name.replace(" ", "_")
    name = name.replace("\n", "")
    name = name.replace("/", "-")

    filepath = Path(gauge + '-' + name + '-' + type + '/data/')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    os.makedirs(filepath, exist_ok=True)

    df["date"] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    #make the daily mean pet and precip files
    df['DOY'] = df['date'].dt.dayofyear
    DOY = df.groupby(['DOY']).mean()
    DOY = DOY.drop([366, 366])
    DOY['pet'].to_csv(str(filepath) + '/evap.txt', index=False)
    DOY['temperature'].to_csv(str(filepath) + '/temp.txt', index=False)

    # Create the PTQ.txt file
    ptq = df.drop(columns=['discharge_vol', 'pet', 'peti','humidity','shortwave_rad','longwave_rad','windspeed','DOY'])
    ptq["date"] = pd.to_datetime(ptq["date"]).dt.strftime('%Y%m%d')
    ptq.to_csv(str(filepath) + '/ptq.txt', index=False, sep="\t")

main()
