#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json

import os
import numpy as np

from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import shutil
from shutil import unpack_archive

import rasterio as rio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.windows import Window
from rasterio.mask import mask

import plotly.graph_objects as go

import streamlit as st


# In[2]:


address = input("Enter full address, including zip code: ")


# In[3]:


def get_coord(address):
    api_url = f"http://loc.geopunt.be/v4/Location?q={address}&c=1"
    response = requests.get(api_url)
    data_json = response.json()
    pt_dict = data_json['LocationResult'][0]["Location"]
    X_Lambert72 = pt_dict['X_Lambert72']
    Y_Lambert72 = pt_dict['Y_Lambert72']
    pt = [X_Lambert72,Y_Lambert72]
    
    return X_Lambert72,Y_Lambert72

def bounds_contains(pt):
    with open('/home/giodsubuntu/3D_house_Lidar/json/new_j_all_bounds.json') as fd:
        d4 = json.load(fd)
        for value in d4.values():
            bounds_box = value
            #if bounds_box[0] < pt[0] < bounds_box[0]+bounds_box[2] and bounds_box[1] < pt[1] < bounds_box[1]+bounds_box[3]:
            if bounds_box[0] < pt[0] < bounds_box[2] and bounds_box[1] < pt[1] < bounds_box[3]:
                break
        for key, value in d4.items():
            if bounds_box == value:
                num = key
                dsm_url = f'https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/DHMVIIDSMRAS1m_k{num}.zip'
                dtm_url = f"https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/DHMVIIDTMRAS1m_k{num}.zip"
                break
                
                   
        return dsm_url,dtm_url

def download_unzip(dtm_url, dsm_url):
        with urlopen(dtm_url) as zipresp, NamedTemporaryFile() as tfile:
            tfile.write(zipresp.read())
            tfile.seek(0)
            filename = dtm_url.split('/')[-1].replace(".zip", "")
            file_path_dtm = f"/home/giodsubuntu/3D_house_Lidar/Files/{filename}"
            unpack_archive(tfile.name,file_path_dtm, format = 'zip')
            tif_dtm = f"{file_path_dtm}/GeoTIFF/{filename}.tif"
        with urlopen(dsm_url) as zipresp, NamedTemporaryFile() as tfile:
            tfile.write(zipresp.read())
            tfile.seek(0)
            filename = dsm_url.split('/')[-1].replace(".zip", "")
            file_path_dsm = f"/home/giodsubuntu/3D_house_Lidar/Files/{filename}"
            unpack_archive(tfile.name,file_path_dsm, format = 'zip')
            tif_dsm = f"{file_path_dsm}/GeoTIFF/{filename}.tif"
        
        return tif_dtm, tif_dsm, file_path_dtm,file_path_dsm
    
def array_dtm(tif_dtm):
    with rio.open(tif_dtm) as rds_dtm:
        row, col = rds_dtm.index(X_Lambert72,Y_Lambert72)
        dtm_slice = (slice(row - 100,row + 100),slice(col -100, col + 100))
        window_dtm = Window.from_slices(*dtm_slice)
        dtm_arr = rds_dtm.read(1, window= window_dtm)
        return dtm_arr


def array_dsm(tif_dsm):
     with rio.open(tif_dsm) as rds_dsm:
        row, col = rds_dsm.index(X_Lambert72,Y_Lambert72)
        dsm_slice = (slice(row - 100,row + 100),slice(col -100, col + 100))
        window_dsm = Window.from_slices(*dsm_slice)
        dsm_arr = rds_dsm.read(1, window= window_dsm)
        return dsm_arr
    
def plot_window(dtm_arr,dsm_arr):
    dtm_arr = array_dtm(tif_dtm)
    dsm_arr = array_dsm(tif_dsm)
    
    chm_window = dsm_arr - dtm_arr
    
    fig = go.Figure(data=[go.Surface(z=chm_window)])
    
    return st.plotly_chart(fig)

#delete the folder
def zip_delete(file_path_dtm,file_path_dsm):
    shutil.rmtree(file_path_dsm, ignore_errors=True)
    shutil.rmtree(file_path_dtm, ignore_errors=True)
    return 
    


# In[ ]:


X_Lambert72,Y_Lambert72 = get_coord(address)
pt = get_coord(address)
dsm_url,dtm_url = bounds_contains(pt)
tif_dtm, tif_dsm, file_path_dtm,file_path_dsm = download_unzip(dtm_url, dsm_url)
dtm_arr = array_dtm(tif_dtm)
dsm_arr = array_dsm(tif_dsm)
plot = plot_window(dtm_arr,dsm_arr)


# In[ ]:


zip_delete(file_path_dtm,file_path_dsm)

