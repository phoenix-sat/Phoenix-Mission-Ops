import sys
import os

from datetime import datetime
from spacetrack import SpaceTrackClient
from params import *
#from db import Database
import numpy as np
from plotly.offline import init_notebook_mode, plot
from plotly.graph_objs import Scatter3d, Line, Data, Layout
import spiceypy as spice
import math
import csv
init_notebook_mode()

DB_NAME = 'satellites'
ref_frame = 'IAU_EARTH'
ref_body = 'EARTH'
sec_factor = 1
et_search_error = 60 # +/- error in seconds when searching for EE indexes

st_login = 'kolby.devery@yahoo.com'
st_pass = 'Thisisaverylongcode'

# Ground Station variables
gs_spk = "kernels/ASU_gs/ASUGS.bsp"
gs_tf = "kernels/ASUGS.tf"
gs_frame = "ASU-GS_TOPO"
gs_min_el = 5.0 # Minimum angle[degrees] above the horizon for the Ground Station
gs_naif_id = "-9999999"

# Variables for the spice.gf function
gf_crdsys = "LATITUDINAL"
gf_coord = "LATITUDE"
gf_relate = ">"
gf_refval = gs_min_el*spice.rpd()
gf_nintvals = 1000
gf_adjust = 0.0
gf_abcorr = "NONE"
gf_step = 30 # Step size for searching for windows

st = None

def sat_naif_id(norad_id):
    return (-100000 - norad_id)

def get_sat_name():
    print('Satellite Name: ')
    name = sys.stdin.readline()
    return str(name).rstrip()

def get_sat_norad():
    print('Satellite NORAD: ')
    norad = sys.stdin.readline()
    return int(norad)

def get_tle(norad_id):
    # Only logs in once...
    global st
    print("\n")
    if(st == None):
        print("Logging into space-track.com...")
        st = SpaceTrackClient(st_login, st_pass)
    print("Retreiving TLE information for NORAD ID " + str(norad_id))
    return st.tle_latest(norad_cat_id=norad_id, format='tle')

def create_tle(sat_name, tle_str, overwrite=False):
    tle_file = "./kernels/ISS/" + sat_name + ".tle"
    isFile = os.path.isfile(tle_file)

    if(len(tle_str) < 50):
        print("Error: incorrect TLE String")
        return
    elif(isFile and overwrite==False):
        print("Error: " + sat_name + ".tle file already exists")
        return
    elif(isFile and overwrite==True):
        print("Warning: Overwritting " + sat_name + ".tle file")
        f = open(tle_file, "w")
    else:
        f = open(tle_file, "x")

    f.write(tle_str)
    f.close()
