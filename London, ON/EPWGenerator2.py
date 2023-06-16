# Program to extract ERA5 reanalysis data into EPW format
# DO NOT USE FOR A LEAP YEAR!
# Developed by: Mohsen Moradi, Amir A. Aliabadi, R. Maeve Mc Leod
# Last modified: 2021 August 13
import xarray as xr
import numpy
import functools
import os
# Some libraries are not needed for this code, but can be later utilized for spatial analysis
'''
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from affine import Affine
from rasterio.warp import transform
from rasterio.plot import show
import fiona
import geopandas as gpd
import csv
import os
from datetime import timedelta
from psychrometrics import psychrometrics
import rasterio
import cdsapi
from netCDF4 import Dataset
'''

def write_epw(StartingTime_ERA5,EndingTime_ERA5,lat_rural,lon_rural,GMT,RawEPW_file,NewEPW_file,ERA5land_file,ERA5_file,
              epw_precision,timeInitial):
    """
    Writing new EPW file
    Note: To convert the UTC to the local time, the ERA5 dataset should include one day before and after
    the starting day and ending day, respectively.
    """
    def WindDirection_deg(U,V):
        angle = numpy.arctan2(V,U)*180/numpy.pi

        if angle < 0:
            WD = 360.0 + angle
        else:
            WD = angle

        return WD

    def RelativeHumidity(T,Tdew):
        # T and Tdew should be in [C]
        RH = 100*(numpy.exp((17.625*Tdew)/(243.04+Tdew))/numpy.exp((17.625*T)/(243.04+T)))
        return RH

    # Read ERA5-land hourly file
    # u10 [m s^-1], v10 [m s^-1], d2m:dew temperature at 2m [K], t2m [K], skt [K], stl1:soil layer temperature at 0-7cm [K],
    # stl2:soil layer temperature at 7-28cm [K], stl3:soil layer temperature at 28-100cm [K], sp: surface pressure [Pa],
    # ssrd: shortwave radiation down [J m^-2], strd: longwave radiation down [J m^-2], tp: total precip [m]
    
    ds_ERA5land = xr.open_dataset(ERA5land_file)

    # Read ERA5 hourly file
    # u10 [m s^-1], v10 [m s^-1], t2m [K], ssrd: Surface solar radiation downwards [J m^-2],
    # strd: Surface thermal radiation downwards [J m^-2] , fdir: Total sky direct solar radiation at surface [J m^-2]
    ds_ERA5 = xr.open_dataset(ERA5_file)


    # Select data that is nearest to the given lat and lon
    ds_ERA5land_Loc = ds_ERA5land.sel(latitude=lat_rural, longitude=lon_rural, method='nearest')
    ds_ERA5_Loc = ds_ERA5.sel(latitude=lat_rural, longitude=lon_rural, method='nearest')
    # Select data that is within the given time window
    ds_ERA5land_Loc_Time = ds_ERA5land_Loc.sel(time=slice(StartingTime_ERA5, EndingTime_ERA5))
    ds_ERA5_Loc_Time = ds_ERA5_Loc.sel(time=slice(StartingTime_ERA5, EndingTime_ERA5))

    # Convert radiations unit from [J m^-2] to [W m^-2]
    nt = len(ds_ERA5land_Loc_Time.time.dt.hour)
    SWR_Wm2 = []
    LWR_Wm2 = []
    SWR_Dir_era5_Wm2 = []
    SWR_Dif_era5_Wm2 = []
    SWR_era5_Wm2 = []
    LWR_era5_Wm2 = []
    Precip_mmh = []
    Pressure_Pa = []
    Tsoil1_C = []
    Tsoil2_C = []
    Tsoil3_C = []
    Tdew_C = []
    T2m_C = []
    U10_ms = []
    V10_ms = []
    S10_ms = []
    WD_deg = []
    RH_100 = []
    for i in range(1,nt):
        if ds_ERA5land_Loc_Time.time.dt.hour[i].values == 1:
            # Total radiation obtained from ERA5-land, which has a spatial resolution of 0.1deg * 0.1deg
            SWR_Wm2.append(ds_ERA5land_Loc_Time.ssrd.isel(time=i).values/3600)
            LWR_Wm2.append(ds_ERA5land_Loc_Time.strd.isel(time=i).values/3600)
            Precip_mmh.append(ds_ERA5land_Loc_Time.tp.isel(time=i).values*1000)
        else:
            # Total radiation obtained from ERA5-land, which has a spatial resolution of 0.1deg * 0.1deg
            SWR_Wm2.append((ds_ERA5land_Loc_Time.ssrd.isel(time=i).values - ds_ERA5land_Loc_Time.ssrd.isel(time=i-1).values)/3600)
            LWR_Wm2.append((ds_ERA5land_Loc_Time.strd.isel(time=i).values - ds_ERA5land_Loc_Time.strd.isel(time=i-1).values)/3600)
            Precip_mmh.append((ds_ERA5land_Loc_Time.tp.isel(time=i).values - ds_ERA5land_Loc_Time.tp.isel(time=i-1).values)*1000)

        # Total, direct, and diffusive radiation obtained from ERA5, which has a spatial resolution of 0.25deg * 0.25deg
        SWR_Dir_era5_Wm2.append(ds_ERA5_Loc_Time.fdir.isel(time=[i]).values[0] / 3600)
        SWR_era5_Wm2.append(ds_ERA5_Loc_Time.ssrd.isel(time=[i]).values[0] / 3600)
        SWR_Dif_era5_Wm2.append(SWR_era5_Wm2[i - 1] - SWR_Dir_era5_Wm2[i - 1])
        LWR_era5_Wm2.append(ds_ERA5_Loc_Time.strd.isel(time=[i]).values[0] / 3600)
        Pressure_Pa.append(ds_ERA5land_Loc_Time.sp.isel(time=i).values)
        Tsoil1_C.append(ds_ERA5land_Loc_Time.stl1.isel(time=i).values-273.15)
        Tsoil2_C.append(ds_ERA5land_Loc_Time.stl2.isel(time=i).values-273.15)
        Tsoil3_C.append(ds_ERA5land_Loc_Time.stl3.isel(time=i).values-273.15)
        Tdew_C.append(ds_ERA5land_Loc_Time.d2m.isel(time=i).values-273.15)
        T2m_C.append(ds_ERA5land_Loc_Time.t2m.isel(time=i).values-273.15)
        U10_ms.append(ds_ERA5land_Loc_Time.u10.isel(time=i).values)
        V10_ms.append(ds_ERA5land_Loc_Time.v10.isel(time=i).values)
        S10_ms.append(numpy.sqrt(U10_ms[i-1]**2+V10_ms[i-1]**2))
        WD_deg.append(WindDirection_deg(V10_ms[i-1],U10_ms[i-1]))
        RH_100.append(RelativeHumidity(T2m_C[i-1],Tdew_C[i-1]))

    # Retrieve the correct environmental data for the local climate
    # UK central time or west of UK
    if GMT <= 0:
        StartingTime = - GMT          # Since GMT is negative, this variable will be strictly positive
        EndingTime = nt
    # East of UK
    else:
        StartingTime = 0
        EndingTime = nt - GMT         # Since GMT is positive, the length of the dataset will be shortened

    SWR_Wm2_localTime = SWR_Wm2[StartingTime:EndingTime]
    LWR_Wm2_localTime = LWR_Wm2[StartingTime:EndingTime]
    SWR_Dir_Wm2_localTime = SWR_Dir_era5_Wm2[StartingTime:EndingTime]
    SWR_Dif_Wm2_localTime = SWR_Dif_era5_Wm2[StartingTime:EndingTime]
    Precip_mmh_localTime = Precip_mmh[StartingTime:EndingTime]
    Pressure_Pa_localTime = Pressure_Pa[StartingTime:EndingTime]
    Tsoil1_C_localTime = Tsoil1_C[StartingTime:EndingTime]
    Tsoil2_C_localTime = Tsoil2_C[StartingTime:EndingTime]
    Tsoil3_C_localTime = Tsoil3_C[StartingTime:EndingTime]
    Tdew_C_localTime = Tdew_C[StartingTime:EndingTime]
    T2m_C_localTime = T2m_C[StartingTime:EndingTime]
    U10_ms_localTime = U10_ms[StartingTime:EndingTime]
    V10_ms_localTime = V10_ms[StartingTime:EndingTime]
    S10_ms_localTime = S10_ms[StartingTime:EndingTime]
    WD_deg_localTime = WD_deg[StartingTime:EndingTime]
    RH_100_localTime = RH_100[StartingTime:EndingTime]
    # Shift the time back to local time zone, note that the month, day, and hour are not used in writing the EPW file
    # UK central time or west of UK
    if GMT <= 0:
        Year_localTime = ds_ERA5land_Loc_Time.time.dt.year.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values
        Month_localTime = ds_ERA5land_Loc_Time.time.dt.month.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values
        Day_localTime = ds_ERA5land_Loc_Time.time.dt.day.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values
        Hour_localTime = ds_ERA5land_Loc_Time.time.dt.hour.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values
    # East of UK
    else:
        Year_localTime = ds_ERA5land_Loc_Time.time.dt.year.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values
        Month_localTime = ds_ERA5land_Loc_Time.time.dt.month.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values
        Day_localTime = ds_ERA5land_Loc_Time.time.dt.day.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values
        Hour_localTime = ds_ERA5land_Loc_Time.time.dt.hour.isel(
            time=slice(StartingTime + GMT, EndingTime + GMT)).values

    month_start = int(StartingTime_ERA5[5:7])
    month_end = int(EndingTime_ERA5[5:7])
    Tdeepsoil_lay1 = []
    Tdeepsoil_lay2 = []
    Tdeepsoil_lay3 = []
    for i in range(month_start,month_end+1):
        Tdeepsoil_lay1.append(ds_ERA5land_Loc_Time.stl1.sel(time=ds_ERA5land_Loc_Time.time.dt.month.isin(i)).mean(keepdims=True).values[0])
        Tdeepsoil_lay2.append(ds_ERA5land_Loc_Time.stl2.sel(time=ds_ERA5land_Loc_Time.time.dt.month.isin(i)).mean(keepdims=True).values[0])
        Tdeepsoil_lay3.append(ds_ERA5land_Loc_Time.stl3.sel(time=ds_ERA5land_Loc_Time.time.dt.month.isin(i)).mean(keepdims=True).values[0])

    # Open .epw file
    with open(RawEPW_file) as f:
        lines = f.readlines()
    climate_data = []
    for i in range(len(lines)):
        climate_data.append(list(lines[i].split(",")))
    _header = climate_data[0:8]
    for i in range(len(Tdeepsoil_lay1)):
        _header[3][i+month_start+5] = str(round(Tdeepsoil_lay1[i]-273.15,2))
        _header[3][i+month_start+21] = str(round(Tdeepsoil_lay2[i]-273.15,2))
        _header[3][i+month_start+37] = str(round(Tdeepsoil_lay3[i]-273.15,2))
    _header[3][2] = str(0.035)
    _header[3][18] = str(0.175)
    _header[3][34] = str(0.64)
    epwinput = climate_data[8:]
    epw_prec = epw_precision  # precision of epw file input

    for iJ in range(len(T2m_C_localTime)):

        # Year
        epwinput[iJ + timeInitial - 8][0] = "{0:}".format(Year_localTime[iJ])
        # dry bulb temperature [C]
        epwinput[iJ + timeInitial - 8][6] = "{0:.{1}f}".format(float(T2m_C_localTime[iJ]), epw_prec)
        # dew point temperature [C]
        epwinput[iJ + timeInitial - 8][7] = "{0:.{1}f}".format(float(Tdew_C_localTime[iJ]), epw_prec)
        # relative humidity [%]
        epwinput[iJ + timeInitial - 8][8] = "{0:.{1}f}".format(float(RH_100_localTime[iJ]), epw_prec)
        # Pressure [Pa]
        epwinput[iJ + timeInitial - 8][9] = "{0:.{1}f}".format(float(Pressure_Pa_localTime[iJ]), epw_prec)
        # LWR [W m^-2]
        epwinput[iJ + timeInitial - 8][12] = "{0:.{1}f}".format(float(LWR_Wm2_localTime[iJ]), epw_prec)
        # SWR_Diff [W m^-2]
        epwinput[iJ + timeInitial - 8][15] = "{0:.{1}f}".format(float(SWR_Dif_Wm2_localTime[iJ]), epw_prec)
        # SWR_Dir [W m^-2]
        epwinput[iJ + timeInitial - 8][14] = "{0:.{1}f}".format(float(SWR_Dir_Wm2_localTime[iJ]), epw_prec)
        # Total global incoming radiation [W m^-2] as the sum of LWR, SWR_Dir, SWR_Diff
        epwinput[iJ + timeInitial - 8][13] = "{0:.{1}f}".format(float(LWR_Wm2_localTime[iJ] + SWR_Dif_Wm2_localTime[iJ] + SWR_Dir_Wm2_localTime[iJ]), epw_prec)
        # Wind Direction [deg]
        epwinput[iJ + timeInitial - 8][20] = "{0:.{1}f}".format(float(WD_deg_localTime[iJ]), epw_prec)
        # wind speed [m s^-1]
        epwinput[iJ + timeInitial - 8][21] = "{0:.{1}f}".format(float(S10_ms_localTime[iJ]), epw_prec)
        # Precipitation [mm h^-1]
        epwinput[iJ + timeInitial - 8][33] = "{0:.{1}f}".format(float(Precip_mmh_localTime[iJ]), 4)

    # Writing new EPW file
    epw_new_id = open(NewEPW_file, "w")

    for i in range(8):
        new_epw_line = '{}'.format(functools.reduce(lambda x, y: x + "," + y, _header[i]))
        epw_new_id.write(new_epw_line)

    for i in range(len(epwinput)):
        printme = ""
        for ei in range(34):
            printme += "{}".format(epwinput[i][ei]) + ','
        printme = printme + "{}".format(epwinput[i][ei])
        new_epw_line = "{0}\n".format(printme)
        epw_new_id.write(new_epw_line)

    epw_new_id.close()

# Note: ERA5-land has the spatial resolution of 0.1x0.1 deg and ERA5 has the spatial resolution of 0.25x0.25. lat and lon
# should be specified carefully to extract data from ERA5 and ERA5-land at the same location.
# Guelph
'''
lat_rural = 43.52360
lon_rural = -80.10370
GMT = -5
# For cities west of UK the starting row for writing data is as follows,
# For cities east of UK add GMT to the initial time, i.e. 8 + GMT
timeInitial = 8 # [JFMAMJJASOND] = [8,752,1424,2168,2888,3632,4352,5096,5840,6560,7304,8023]
'''
# Toronto
# '''
lat_rural = -42.976
lon_rural = -81.471
GMT = -5
# For cities west of UK the starting row for writing data is as follows,
# For cities east of UK add GMT to the initial time, i.e. 8 + GMT
# timeInitial = 8023 # [JFMAMJJASOND] = [8,752,1424,2168,2888,3632,4352,5096,5840,6560,7304,8023]

# StartingTime_ERA5 = '2007-12-01'
# EndingTime_ERA5 = '2007-12-31'

# '''
# Always the content from the NewEPW_file are appended to the RawEPW_file
# So for appending of consecutive periods to an existing EPW file,
# keep updating the RawEPW_file to the latest file created in the last step
# RawEPW_file = 'ERA5_London_Nov2007.epw'
# NewEPW_file = 'ERA5_London_Dec2007.epw'
# ERA5land_file = 'ERA5Land\ERA5Land_2007_Dec.nc'
# ERA5_file = 'ERA5\ERA5_2007_Dec.nc'
# # Number of decimal points for writing the data, except for precipitattion. DO NOT CHANGE
# epw_precision = 1
# # Starting row at which the new information will be written in the EPW file. Select the appropriate month


# write_epw(StartingTime_ERA5,EndingTime_ERA5,lat_rural,lon_rural,GMT,RawEPW_file,NewEPW_file,ERA5land_file,ERA5_file,epw_precision,timeInitial)

year = "1980"
city = "London" 
# # Testing to see if i can speed up the process

# Create the subdirectory if it doesn't exist
if not os.path.exists("EPW Files/" + year):
    os.makedirs("EPW Files/"+year)

write_epw(year+"-01-01",year+"-01-31",lat_rural,lon_rural,GMT,"rawEPW.epw","EPW Files/"+year+"/ERA5_"+city+"_Jan"+year+".epw","ERA5Land/ERA5Land_"+year+"_Jan.nc","ERA5/ERA5_"+year+"_Jan.nc",1,8)
write_epw(year+"-02-01",year+"-02-28",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Jan"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Feb"+year+".epw","ERA5Land/ERA5Land_"+year+"_Feb.nc","ERA5/ERA5_"+year+"_Feb.nc",1,752)
write_epw(year+"-03-01",year+"-03-31",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Feb"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Mar"+year+".epw","ERA5Land/ERA5Land_"+year+"_Mar.nc","ERA5/ERA5_"+year+"_Mar.nc",1,1424)
write_epw(year+"-04-01",year+"-04-30",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Mar"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Apr"+year+".epw","ERA5Land/ERA5Land_"+year+"_Apr.nc","ERA5/ERA5_"+year+"_Apr.nc",1,2168)
write_epw(year+"-05-01",year+"-05-31",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Apr"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_May"+year+".epw","ERA5Land/ERA5Land_"+year+"_May.nc","ERA5/ERA5_"+year+"_May.nc",1,2888)
write_epw(year+"-06-01",year+"-06-30",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_May"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Jun"+year+".epw","ERA5Land/ERA5Land_"+year+"_Jun.nc","ERA5/ERA5_"+year+"_Jun.nc",1,3632)
write_epw(year+"-07-01",year+"-07-31",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Jun"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Jul"+year+".epw","ERA5Land/ERA5Land_"+year+"_Jul.nc","ERA5/ERA5_"+year+"_Jul.nc",1,4352)
write_epw(year+"-08-01",year+"-08-31",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Jul"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Aug"+year+".epw","ERA5Land/ERA5Land_"+year+"_Aug.nc","ERA5/ERA5_"+year+"_Aug.nc",1,5096)
write_epw(year+"-09-01",year+"-09-30",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Aug"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Sep"+year+".epw","ERA5Land/ERA5Land_"+year+"_Sep.nc","ERA5/ERA5_"+year+"_Sep.nc",1,5840)
write_epw(year+"-10-01",year+"-10-31",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Sep"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Oct"+year+".epw","ERA5Land/ERA5Land_"+year+"_Oct.nc","ERA5/ERA5_"+year+"_Oct.nc",1,6560)
write_epw(year+"-11-01",year+"-11-30",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Oct"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Nov"+year+".epw","ERA5Land/ERA5Land_"+year+"_Nov.nc","ERA5/ERA5_"+year+"_Nov.nc",1,7304)
write_epw(year+"-12-01",year+"-12-31",lat_rural,lon_rural,GMT,"EPW Files/"+year+"/ERA5_"+city+"_Nov"+year+".epw","EPW Files/"+year+"/ERA5_"+city+"_Dec"+year+".epw","ERA5Land/ERA5Land_"+year+"_Dec.nc","ERA5/ERA5_"+year+"_Dec.nc",1,8023)