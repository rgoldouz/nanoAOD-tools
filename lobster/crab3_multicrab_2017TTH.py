#!/usr/bin/env python
import os
import sys
import re
import string
sys.path.append(os.path.abspath("."))
import Files_2017
os.system('source /cvmfs/cms.cern.ch/crab3/crab.sh')

SAMPLES = {}
UL_YEAR = 'UL17'

if UL_YEAR=='UL17':
    SAMPLES.update(Files_2017.mc2017_samples)
    SAMPLES.update(Files_2017.data2017_samples)

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand

    def submit(config):
        res = crabCommand('submit', config = config)

    from CRABClient.UserUtilities import config
    config = config()

    name = 'NanoAodPostProcessingUL'
    config.General.workArea = 'crab_'+name
    config.General.transferLogs = False
    config.General.transferOutputs = True
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.scriptExe  = 'crab_script.sh'
    config.JobType.inputFiles = ['Lobster_postproc.py', '../scripts/haddnano.py','Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt' ]
    config.JobType.sendPythonFolder        = True
    config.JobType.allowUndistributedCMSSW = True
    config.Data.splitting     = 'FileBased'
    config.Data.inputDBS      = 'global'
    config.Site.storageSite = 'T3_US_NotreDame'
    config.Data.unitsPerJob = 1
    config.Data.publication = False

    for key, value in SAMPLES.items():
        print key
        config.General.requestName = key
        config.Data.inputDataset = value[0][0]
        config.Data.outLFNDirBase = '/store/user/rgoldouz/NanoAodPostProcessingUL/UL17/v1/' + key
        config.JobType.scriptArgs  = ['--DataProcessing=' + value[1],'--year=' + value[2], '--run=' +  value[3], '--json=' + value[4], '--crab=True']
        submit(config)
