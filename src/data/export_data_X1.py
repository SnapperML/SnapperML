#!/usr/bin/env python

"""
 This script saves the data as the 9 traces of each SiPM

 """

import ROOT
from ROOT import TFile, TTree, TH1D, AddressOf, TCanvas, gPad
from ROOT import kBlack, kBlue, kRed, kGreen

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd


path_lib = "/LATTESsim/libEventROOT.so"
bool_val = ROOT.gSystem.Load(path_lib)

# Define the number of PMTs in the station
PMTNUMBER = 9

# comment nentries to run over all file
totalEntries = 240     #maximum of 3693
TrainEntries = 120

# trace length in nanoseconds
traceLength = 9

#inputfilename = './input_files/newconcept_bin_3_1.root'
inputfilename = './data/raw/proton_bin_3_4_newconcept.root'
outputfilename = './data/X1_proton_3_4_TL'+str(traceLength)+'_N'+str(TrainEntries)+'.csv'
outputfilenameSingle = './data/X1_proton_SingleMuon_3_4_TL'+str(traceLength)+'_N'+str(TrainEntries)+'.csv'
outputfilenameTest = './data/X1_test_proton_3_4_TL'+str(traceLength)+'_N'+str(totalEntries-TrainEntries)+'.csv'

f = TFile(inputfilename)
f.ls()
t = f.Get("Tree")

nbins = 310
hTrace = TH1D("AverageTrace",";t (ns)",nbins,-10.0,300.0)

e = ROOT.EventROOT();

#StationROOT s;
#PMTROOT pmt;

NEVENTS = 0
ie = 0
NSTATIONS = 0

t.SetBranchAddress("EventROOT",AddressOf(e));
nentries = t.GetEntriesFast()
print('nentries',nentries)

def FillTraceROOT(pmt, hTrace,tStart):
    time = 0.0
    trace = pmt.GetTrace()
    for trace_iter in trace:
        time = trace_iter.first
        hTrace.Fill(time - tStart, trace_iter.second)
    return

def FillTracePy(pmt, SumTrace, tStart):
    time = 0.0
    trace = pmt.GetTrace()
    for trace_iter in trace:
        time = trace_iter.first
        SumTrace.append([(time - tStart),trace_iter.second])
    return


# defines a fixed array of limit size and updates index with signal recorded

def SimpleFillTracePy(pmt, tStart, limit = 30):

    #make row of limit nanoseconds
    FilledSumTrace = np.zeros(limit)

    time = 0.0
    trace = pmt.GetTrace()
    for trace_iter in trace:
        time = trace_iter.first
        idx=int(time - tStart)
        if idx<limit:
            FilledSumTrace[idx] = trace_iter.second
    return FilledSumTrace



ie = 0

FilledSumTrace = []

SumTrace = []

#pbar = tqdm_notebook(total = nentries)

# output_file = open(outputfilename, 'w', newline='')
# wr = csv.writer(output_file)#, dialect='excel')
data_dump = []
data_dumpSM = []
data_dumpTest = []


NumbStationMuons = 0
NumbStationMuonsSingle = 0

contTrainEntries = 0

# loop over showers
while (ie < nentries and contTrainEntries < totalEntries):
    t.GetEntry(int(ie))
    #pbar.update(1)

    print("processing shower: ",ie,"/",totalEntries,"Number of stations with muons", NumbStationMuons, "Single Muons", NumbStationMuonsSingle)

    NEVENTS += 1
    ie += 1
    shower_id = ie
    contTrainEntries += 1

    #event info
    E0 = e.GetCORSIKAEvent().EPRI
    primary = e.GetCORSIKAEvent().PRIM

    # loop over WCD stations
    nextStation = ROOT.TIter(e.GetStations())
    myNSTATIONS = 0
    while True:
        s = nextStation()
        if not s :
            break
        core = e.GetCorePosition()
        #print(ie, s.GetPosition().x())

        # For a test consider only stations close to the core
        #if (s.GetPosition() - core).Perp() > 10.0:
        #    continue

        nb_muons = s.GetNMuons()
        nb_electrons = s.GetNElectrons()
        nb_photons = s.GetNPhotons()
        nb_optical = s.GetNOpticalHits()

        if nb_optical == 0:
            continue

        if nb_muons > 0:
            #print(nb_muons, nb_electrons, nb_photons)
            NumbStationMuons += 1
            if nb_electrons == 0 and nb_photons == 0:
                NumbStationMuonsSingle += 1



        NSTATIONS += 1
        myNSTATIONS += 1
        tStart = ROOT.TMath.Floor(s.GetStartTime())

        traces=[]
        # loop over PMTs in WCD station
        pmts = ROOT.TIter(s.GetPMTs())
        PMTcounter = 0
        FullTrace = np.zeros(traceLength*PMTNUMBER)
        while True:
            pmt = pmts()
            PMTcounter += 1

            if not pmt:
                break

            pmt_id = pmt.GetID() - 1
            pmt_pos = pmt.GetPosition()

            #place the trace generated where it corresponds respect the SiPM id
            FullTrace[traceLength*pmt_id:traceLength*(pmt_id+1)] = SimpleFillTracePy(pmt,tStart,traceLength)

        #print([contTrainEntries,TrainEntries,traces,nb_muons])
        if contTrainEntries <= TrainEntries:
            if nb_muons == 0:
                data_dump.append(np.concatenate((shower_id,myNSTATIONS,FullTrace,0),axis=None))
                data_dumpSM.append(np.concatenate((shower_id,myNSTATIONS,FullTrace,0),axis=None))
            else:
                data_dump.append(np.concatenate((shower_id,myNSTATIONS,FullTrace,1),axis=None))

                if nb_electrons == 0 and nb_photons == 0:
                    data_dumpSM.append(np.concatenate((shower_id,myNSTATIONS,FullTrace,1),axis=None))


        else:
            if nb_muons == 0:
                data_dumpTest.append(np.concatenate((shower_id,myNSTATIONS,FullTrace,0),axis=None))
            else:
                data_dumpTest.append(np.concatenate((shower_id,myNSTATIONS,FullTrace,1),axis=None))


        del FullTrace
        del FilledSumTrace
        FilledSumTrace = []
        #print("Dumped info for shower",shower_id,"Station ", myNSTATIONS)
        #print(data_dump)

    if contTrainEntries == TrainEntries:
        print("Writting to disk...")
        data_dumpDf = pd.DataFrame(data_dump)
        data_dumpDf.to_csv(outputfilename, index=False)

        del data_dumpDf
        del data_dump

        data_dumpDf = pd.DataFrame(data_dumpSM)
        data_dumpDf.to_csv(outputfilenameSingle, index=False)

        del data_dumpDf
        del data_dumpSM


print("Writting to disk test...")
data_dumpTestDf = pd.DataFrame(data_dumpTest)
data_dumpTestDf.to_csv(outputfilenameTest, index=False)
