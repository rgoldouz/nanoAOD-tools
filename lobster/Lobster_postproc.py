#!/usr/bin/env python
import os
import sys
import re
import string
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2  import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.etop.skimModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.lepTop.lepTopskimModule import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputFiles")
    parser.add_option("-s", "--postfix", dest="postfix", type="string", default=None,
                      help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_option("-J", "--json", dest="json", type="string",
                      default=None, help="Select events using this JSON file")
    parser.add_option("-c", "--cut", dest="cut", type="string",
                      default=None, help="Cut string")
    parser.add_option("-b", "--branch-selection", dest="branchsel",
                      type="string", default=None, help="Branch selection")
    parser.add_option("--bi", "--branch-selection-input", dest="branchsel_in",
                      type="string", default=None, help="Branch selection input")
    parser.add_option("--bo", "--branch-selection-output", dest="branchsel_out",
                      type="string", default=None, help="Branch selection output")
    parser.add_option("--friend", dest="friend", action="store_true", default=False,
                      help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full", dest="friend", action="store_false", default=False,
                      help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout", dest="noOut", action="store_true",
                      default=False, help="Do not produce output, just run modules")
    parser.add_option("-P", "--prefetch", dest="prefetch", action="store_true", default=False,
                      help="Prefetch input files locally instead of accessing them via xrootd")
    parser.add_option("--long-term-cache", dest="longTermCache", action="store_true", default=False,
                      help="Keep prefetched files across runs instead of deleting them at the end")
    parser.add_option("-N", "--max-entries", dest="maxEntries", type="long", default=None,
                      help="Maximum number of entries to process from any single given input tree")
    parser.add_option("--first-entry", dest="firstEntry", type="long", default=0,
                      help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_option("--justcount", dest="justcount", default=False,
                      action="store_true", help="Just report the number of selected events")
    parser.add_option("-I", "--import", dest="imports", type="string", default=[], action="append",
                      nargs=2, help="Import modules (python package, comma-separated list of ")
    parser.add_option("-z", "--compression", dest="compression", type="string",
                      default=("LZMA:9"), help="Compression: none, or (algo):(level) ")
    parser.add_option("-y", "--year", dest="year", type="string",
                      default=("UL2017"), help="Which year do you run on? ")
    parser.add_option("-d", "--DataProcessing", dest="DataProcessing", type="string",
                      default=("mc"), help="Which dataset do you run on? data or mc? ")
    parser.add_option("-r", "--run", dest="run", type="string",
                      default=("mc"), help="Which run period do you run on?")
    parser.add_option("-H", "--crab", dest="crab", type="string",
                      default=("False"), help="Which run period do you run on?")
    (options, args) = parser.parse_args()


year=options.year
moduleList = []
outdir=[]
args=[]
if options.crab!='True':
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    outdir = args[0]
    args = args[1:]

if options.DataProcessing == 'mc':
    btagSF_deepcsv = lambda: btagSFProducer(era=year,algo="deepcsv", selectedWPs=["L", "M", "T"], sfFileName="DeepCSV_106XUL" + year[4:] + "SF_WPonly.csv")
    btagSF_deepjet = lambda: btagSFProducer(era=year,algo="deepjet", selectedWPs=["L", "M", "T"], sfFileName="DeepJet_106XUL" + year[4:] + "SF_WPonly.csv")
    if "2016" in year:
        jetmetCorrector = createJMECorrector(isMC=True, dataYear=year, jetType="AK4PFchs" , splitJER=True, jesUncert="All" )
        moduleList = [lepTopskimModuleConstr(), jetmetCorrector(), puWeight_UL2016(), PrefCorr(), btagSF_deepcsv(), btagSF_deepjet()]
    if "2017" in year:
        jetmetCorrector = createJMECorrector(isMC=True, dataYear=year, jetType="AK4PFchs" , splitJER=True, jesUncert="All" )
        moduleList = [lepTopskimModuleConstr(), jetmetCorrector(), puWeight_UL2017(), PrefCorr(), btagSF_deepcsv(), btagSF_deepjet()]
    if "2018" in year:
        jetmetCorrector2018 = createJMECorrector(isMC=True, dataYear=year, jetType="AK4PFchs" , splitJER=True, jesUncert="All", applyHEMfix=True )
        moduleList = [lepTopskimModuleConstr(), jetmetCorrector2018(), puWeight_UL2018(), btagSF_deepcsv(), btagSF_deepjet()]
    if options.crab == 'True':
        p=PostProcessor(outdir, inputFiles=inputFiles(), modules=moduleList, provenance=True, fwkJobReport=True) #, outputbranchsel="keep_and_drop.txt")
    else:
        p=PostProcessor(outdir, args, modules=moduleList, provenance=True, fwkJobReport=True) #, outputbranchsel="keep_and_drop.txt")
else:
    jetmetCorrectorData = createJMECorrector(isMC=False, dataYear=year, runPeriod=options.run, jetType="AK4PFchs")
    moduleList = [lepTopskimModuleConstr(), jetmetCorrectorData()]
    if options.crab== 'True':
        p=PostProcessor(outdir, inputFiles=inputFiles(), jsonInput=options.json, modules=moduleList, provenance=True, fwkJobReport=True)
    else:
        p=PostProcessor(outdir, args, jsonInput=options.json, modules=moduleList, provenance=True, fwkJobReport=True)

p.run()

print("DONE")
