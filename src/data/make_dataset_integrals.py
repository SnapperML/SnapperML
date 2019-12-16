"""
 This script saves the data as the 9 integrals of each SiPM
 """

import ROOT
from ROOT import TFile, TTree, TH1D, AddressOf, TCanvas, gPad
import numpy as np
import pandas as pd
import os
from src.utils.cli import cli_decorator

path_lib = "/LATTESsim/libEventROOT.so"
bool_val = ROOT.gSystem.Load(path_lib)

# Define the number of PMTs in the station
PMTNUMBER = 9

# comment nentries to run over all file
totalEntries = 2500  # maximum of 3693
TrainEntries = 1500

# trace length in nanoseconds
integralTL = 3


def integrate_trace(pmt, tStart, limit=30):
    """Computes the integral from 0 to the limit specified"""
    result = 0.0
    trace = pmt.GetTrace()
    for trace_iter in trace:
        time = trace_iter.first
        idx = int(time - tStart)
        if idx < limit:
            result += trace_iter.second
    return result


def print_trace(pmt, tStart):
    print("----------- Integral == 0 --------------------------")
    trace = pmt.GetTrace()
    for trace_iter in trace:
        time = trace_iter.first
        print("tStart", tStart, "Time: ", time, "iter scnd: ", trace_iter.second)


@cli_decorator
def main(input_folder, output_folder):
    input_filename = os.path.join(input_folder, 'proton_bin_3_4_newconcept.root')
    output_filename_train = os.path.join(
        output_folder,
        f'X2_proton_3_4_TL{integralTL}_N{TrainEntries}.csv')
    output_filename_single = os.path.join(
        output_folder,
        f'X2_proton_SingleMuon_3_4_TL{integralTL}_N{TrainEntries}.csv')
    output_filename_test = os.path.join(
        output_folder,
        f'X2_test_proton_3_4_SingleMuon_TL{integralTL}_N{totalEntries - TrainEntries}.csv')

    f = TFile(input_filename)
    f.ls()
    t = f.Get("Tree")
    e = ROOT.EventROOT()

    NEVENTS = 0
    NSTATIONS = 0

    t.SetBranchAddress("EventROOT", AddressOf(e))
    nentries = t.GetEntriesFast()
    print('nentries', nentries)

    ie = 0
    data_dump = []
    data_dumpSM = []
    data_dumpTest = []

    NumbStationMuons = 0
    NumbStationMuonsSingle = 0

    contTrainEntries = 0

    # loop over showers
    while ie < nentries and contTrainEntries < totalEntries:
        t.GetEntry(int(ie))

        print("processing shower: ", ie, "/", totalEntries, "Number of stations with muons", NumbStationMuons,
              "Single Muons", NumbStationMuonsSingle)

        NEVENTS += 1
        ie += 1
        shower_id = ie
        contTrainEntries += 1

        # loop over WCD stations
        nextStation = ROOT.TIter(e.GetStations())
        myNSTATIONS = 0
        while True:
            s = nextStation()
            if not s:
                break
            core = e.GetCorePosition()
            nb_muons = s.GetNMuons()
            nb_electrons = s.GetNElectrons()
            nb_photons = s.GetNPhotons()
            nb_optical = s.GetNOpticalHits()

            if nb_optical == 0:
                continue

            if nb_muons > 0:
                NumbStationMuons += 1
                if nb_electrons == 0 and nb_photons == 0:
                    NumbStationMuonsSingle += 1

            NSTATIONS += 1
            myNSTATIONS += 1
            tStart = ROOT.TMath.Floor(s.GetStartTime())

            traces = []
            # loop over PMTs in WCD station
            pmts = ROOT.TIter(s.GetPMTs())
            PMTcounter = 0
            FullIntegrals = np.zeros(PMTNUMBER)
            while True:
                pmt = pmts()
                PMTcounter += 1

                if not pmt:
                    break

                pmt_id = pmt.GetID() - 1
                FullIntegrals[pmt_id] = integrate_trace(pmt, tStart, integralTL)

            if np.sum(FullIntegrals) == 0:
                print("Founded station with 0 signal... station: ", myNSTATIONS, "FullIntegrals", FullIntegrals,
                      "nb optical ", nb_optical)

                pmts = ROOT.TIter(s.GetPMTs())

                while True:
                    pmt = pmts()
                    PMTcounter += 1
                    if not pmt:
                        break
                    print_trace(pmt, tStart, integralTL)

            if contTrainEntries <= TrainEntries:
                if nb_muons == 0:
                    data_dump.append(np.concatenate((shower_id, myNSTATIONS, FullIntegrals, 0), axis=None))
                    data_dumpSM.append(np.concatenate((shower_id, myNSTATIONS, FullIntegrals, 0), axis=None))
                else:
                    data_dump.append(np.concatenate((shower_id, myNSTATIONS, FullIntegrals, 1), axis=None))
                    if not nb_electrons and not nb_photons:
                        data_dumpSM.append(np.concatenate((shower_id, myNSTATIONS, FullIntegrals, 1), axis=None))
            else:
                if nb_muons == 0:
                    data_dumpTest.append(np.concatenate((shower_id, myNSTATIONS, FullIntegrals, 0), axis=None))
                elif not nb_electrons and not nb_photons:
                    data_dumpTest.append(np.concatenate((shower_id, myNSTATIONS, FullIntegrals, 1), axis=None))

            del FullIntegrals

        if contTrainEntries == TrainEntries:
            print("Writing to disk...")
            data_dumpDf = pd.DataFrame(data_dump)
            data_dumpDf.to_csv(output_filename_train, index=False)

            del data_dumpDf
            del data_dump

            data_dumpDf = pd.DataFrame(data_dumpSM)
            data_dumpDf.to_csv(output_filename_single, index=False)

            del data_dumpDf
            del data_dumpSM

    print("Writing to disk test...")
    data_dumpTestDf = pd.DataFrame(data_dumpTest)
    data_dumpTestDf.to_csv(output_filename_test, index=False)


if __name__ == '__main__':
    main()
