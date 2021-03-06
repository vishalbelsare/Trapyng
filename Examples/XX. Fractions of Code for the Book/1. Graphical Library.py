""" EXPERIMENTAL INDICATORS """
# Change main directory to the main folder and import folders
import os
os.chdir("../")
import import_folders
# Classical Libraries
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import copy as copy
import pylab
# Own graphical library
from graph_lib import gl
import graph_tsa as grtsa
# Data Structures Data
import CTimeData as CTD
# Import functions independent of DataStructure
import utilities_lib as ul
import indicators_lib as indl
import indicators_pandas as indp
import oscillators_lib as oscl
import basicMathlib as bMA
plt.close("all") # Close all previous Windows
######## SELECT DATASET, SYMBOLS AND PERIODS ########
dataSource =  "GCI"  # Hanseatic  FxPro GCI Yahoo
[storage_folder, info_folder, 
 updates_folder] = ul.get_foldersData(source = dataSource)

symbols = ["XAUUSD","Mad.ITX", "EURUSD"]
symbols = ["Alcoa_Inc"]
symbols = ["Amazon"]
periods = [1440]
######## SELECT DATE LIMITS ###########
sdate_str = "01-01-2016"; edate_str = "2-1-2017"
sdate = dt.datetime.strptime(sdate_str, "%d-%m-%Y")
edate = dt.datetime.strptime(edate_str, "%d-%m-%Y")
######## CREATE THE OBJECT AND LOAD THE DATA ##########
# Tell which company and which period we want
timeData = CTD.CTimeData(symbols[0],periods[0])
timeData.set_csv(storage_folder)  # Load the data into the model
timeData.set_interval(sdate,edate) # Set the interval period to be analysed


    
MOM_ROC_f = 1
ACFE = 0
STO_f = 0
TRIX_f = 0
RSI_f = 0
folder_images = "./pics/Trapying/Oscillators/"

if (MOM_ROC_f == 1):
################# ROC and MOM #######################
    
    price = timeData.get_timeSeries(["Close"]);
    dates = timeData.get_dates()
    df = timeData.get_timeData()
    
    # Momentum and Rate of convergence
    nMOM = 20
    nROC = 20
    
    MOM = timeData.MOM(n = nMOM)
    ROC = timeData.ROC(n = nROC)
    
    # Plotting
    gl.set_subplots(2,1)
    
    gl.plot(dates, price , nf = 1,
            labels = ["Momentum Indicators MOM and ROC","","Price"],
            legend = ["Price", " Momentum", "ROC"])
            
    gl.plot(dates, MOM , nf = 1, na = 0,
            legend = ["MOM(%i)"%nMOM])
    
    # Normalize ROC to MOM
    ROC = ROC * np.max(np.abs(np.nan_to_num(MOM)))/  np.max(np.abs(np.nan_to_num(ROC)))
    gl.plot(dates, ROC, nf = 0, na = 0,
            legend = ["ROC(%i)"%nROC])
    # The nect plot is just so that the vision starts in the first date
    gl.plot(dates, np.zeros((dates.size,1)) , nf = 0, na = 0)
 
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)

    gl.savefig(folder_images +'OscillatorsMOM.png', 
               dpi = 100, sizeInches = [2*8, 2*2])
               
               
    
    price = timeData.get_timeSeries(["Close"]);
    dates = timeData.get_dates()
    df = timeData.get_timeData()
    
    # Momentum and Rate of convergence obtained from the real price.
    nMOMs = [10, 20, 30]
    MOM1 = timeData.MOM(n = 1)
    
    
    EMAMOMs = [indl.get_EMA(MOM1, nMOMi) for nMOMi in nMOMs]
    
    # Normalize ROC to MOM
    gl.set_subplots(2,1)
    
    gl.plot(dates, price , nf = 1,
            labels = ["Smoothed MOM(1)","","Price"],
            legend = ["Price", " Momentum", "ROC"])
            
    legend = ["EMA(MOM(1),%i)"%x for x in nMOMs]
    gl.plot(dates, EMAMOMs , nf = 1, na = 0,
            legend = legend)
            
    # The nect plot is just so that the vision starts in the first date
    gl.plot(dates, np.zeros((dates.size,1)) , nf = 0, na = 0)
 
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)

    gl.savefig(folder_images +'OscillatorsSmoothedMOM.png', 
               dpi = 100, sizeInches = [2*8, 2*2])
               

if (ACFE == 1):
      
    price = timeData.get_timeSeries(["Close"]);
    dates = timeData.get_dates()
    df = timeData.get_timeData()
    # Momentum and Rate of convergence
    nAD = 5
    ACCDIST = timeData.ACCDIST(n = nAD)
    
    # Plotting
    gl.set_subplots(2,1)
    gl.plot(dates, price , nf = 1,
            labels = ["Momentum Indicators ACC DIST","","Price"],
            legend = ["Price", " Momentum", "ROC"])
    
    vol = timeData.get_timeSeries(["Volume"])
    gl.stem(dates, vol , nf = 0, na = 1,
            legend = ["Volume"])
            
            
    gl.plot(dates, ACCDIST , nf = 1, na = 0,
            legend = ["ACCDIST(%i)"%nMOM])
    gl.plot(dates, np.zeros((dates.size,1)) , nf = 0, na = 0)
 
    
 
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)

    gl.savefig(folder_images +'AC.png', 
               dpi = 100, sizeInches = [2*8, 2*2])

#########################################################
# Oscillators 
if (STO_f):
    price = timeData.get_timeSeries(["Close"]);
    dates = timeData.get_dates()
    df = timeData.get_timeData()
    
    n , SK, SD = 14, 6,6
    STO = timeData.STO(n = n, SK = SK, SD = SD)

    gl.set_subplots(2,1)
    gl.plot(dates, price , nf = 1,
            labels = ["Stochastic Oscillator STO(%i,%i,%i)"%(n,SK,SD),"","Price"],
            legend = ["Price"])
            
    gl.plot(dates, STO, nf = 1, na = 0,
            labels = ["","","Oscillator"],
            legend = ["STOk(%i,%i)"%(n,SK), "STOd(%i)"%(SD)])

    # The nect plot is just so that the vision starts in the first date
    gl.plot(dates, np.zeros((dates.size,1)) , nf = 0, na = 0)
 
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)

    gl.savefig(folder_images +'OscillatorsSTO.png', 
               dpi = 100, sizeInches = [2*8, 2*2])


if (TRIX_f):
    price = timeData.get_timeSeries(["Close"]);
    dates = timeData.get_dates()
    df = timeData.get_timeData()
    
    L1 , L2, L3 = 14, 9,12
    EX1,EX2,EX3,TRIX = timeData.TRIX(L1 , L2, L3)

    gl.set_subplots(2,1)
    gl.plot(dates, price , nf = 1,
            labels = ["TRIX oscillator(%i,%i,%i)"%(L1,L2, L3),"","Price"],
            legend = ["Price"])
            
    gl.plot(dates, [EX1,EX2,EX3] , nf = 0,
            legend = ["EMA1(%i)"%L1, "EMA2(%i)"%L2, "EMA3(%i)"%L3])
            
    gl.plot(dates, TRIX, nf = 1, na = 0,
            labels = ["","","Oscillator"],
            legend = ["TRIX(%i,%i,%i)"%(L1,L2, L3)])

    # The nect plot is just so that the vision starts in the first date
    gl.plot(dates, np.zeros((dates.size,1)) , nf = 0, na = 0)
 
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)

    gl.savefig(folder_images +'OscillatorsTRIX.png', 
               dpi = 100, sizeInches = [2*8, 2*2])

if (RSI_f):
    price = timeData.get_timeSeries(["Close"]);
    dates = timeData.get_dates()
    df = timeData.get_timeData()
    
    L = 14
    RS, RSI = timeData.RSI(n = L)
#    RSI2 = oscl.get_RSI2(price, n = L)
    
    gl.set_subplots(2,1)
    gl.plot(dates, price , nf = 1,
            labels = ["RSI oscillator(%i)"%(L),"","Price"],
            legend = ["Price"])
            
    gl.plot(dates, RSI , nf = 1,
            legend = ["RSI1(%i)"%L])
    gl.plot(dates, RS , nf = 0, na = 1,
            legend = ["RS1(%i)"%L]) 
#    gl.plot(dates, RSI2 , nf = 0, na = 1,
#            legend = ["RSI2(%i)"%L])

    # The nect plot is just so that the vision starts in the first date
    gl.plot(dates, np.zeros((dates.size,1)) , nf = 0, na = 0)
 
    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)

    gl.savefig(folder_images +'OscillatorsRSI.png', 
               dpi = 100, sizeInches = [2*8, 2*2])
               
