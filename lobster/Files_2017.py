import sys 
import os 
import subprocess 
import readline 
import string 


mc2017_samples = {
#    "UL17_DY10to50" : [["/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_DY50" : [["/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-Pilot_106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_ST_top_schannel" : [[ "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_ST_top_tchannel" : [["/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_ST_antitop_tchannel" : [[ "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_tbarW" : [["/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_tW" : [["/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_TTJets" : [[ "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_TTTo2L2Nu" : [[ "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_WJetsToLNu" : [["/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_WWTo2L2Nu" : [[ "/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_WWW_4F" : [[ "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_WWZ_4F" : [[ "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_WZTo3LNu" : [[ "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_WZTo2L2Q" : [["/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_ZZTo2L2Nu" : [["/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
    "UL17_WZZ" : [["/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_ZZTo4L" : [["/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'], # NOTE: V8
#    "UL17_ZZZ" : [["/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_TTWJetsToLNu" : [["/TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_TTZToLLNuNu_M_10" : [["/TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],
#    "UL17_BNV_TT_TBUE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_TT_TBUE"], "mc", "UL2017", '1','j', 'hadoop'],  
#    "UL17_BNV_TT_TSCE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_TT_TSCE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_TT_TSUE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_TT_TSUE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_ST_TSCE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_ST_TSCE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_TT_TBCE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_TT_TBCE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_TT_TDUE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_TT_TDUE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_ST_TDUE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_ST_TDUE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_ST_TDCE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_ST_TDCE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_ST_TBUE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_ST_TBUE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_ST_TBCE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_ST_TBCE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_ST_TSUE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_ST_TSUE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_BNV_TT_TDCE" : [["rgoldouz/FullProduction/FullR2/UL17/TopBNV/postLHE_step/v1/nAOD_step_BNV_TT_TDCE"], "mc", "UL2017", '1','j', 'hadoop'],
#    "UL17_tuFCNC_tHProduction" : [["rgoldouz/FullProduction/FullR2/UL17/Round1/Batch3/postLHE_step/v1/nAOD_step_tuFCNC_tHProduction"], "mc", "UL2017", '1','j', 'hadoop'],  
#    "UL17_tuFCNC_tllProduction" : [["rgoldouz/FullProduction/FullR2/UL17/Round1/Batch3/postLHE_step/v1/nAOD_step_tuFCNC_tllProduction"], "mc", "UL2017", '1','j', 'hadoop'], 
#    "UL17_tuFCNC_uHDecay" : [["rgoldouz/FullProduction/FullR2/UL17/Round1/Batch3/postLHE_step/v1/nAOD_step_tuFCNC_uHDecay"], "mc", "UL2017", '1','j', 'hadoop'],       
#    "UL17_tuFCNC_ullDecay" : [["rgoldouz/FullProduction/FullR2/UL17/Round1/Batch3/postLHE_step/v1/nAOD_step_tuFCNC_ullDecay"], "mc", "UL2017", '1','j', 'hadoop'],
}

#    "UL17_WZZ" : [["/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM","/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9_ext1-v2/NANOAODSIM"], "mc", "UL2017", '1','j', 'DAS'],

data2017_samples={}
#'2017_B_SingleMuon': [['rgoldouz/ExitedTopSamplesDataJan2021/SingleMuon/crab_2017_B_SingleMuon/210502_205605/0000'], 'data', 'SingleMuon', '2017', 'B', '1', '1', '1'], '2017_F_SinglePhoton': [['rgoldouz/ExitedTopSamplesDataJan2021/SinglePhoton/crab_2017_F_SinglePhoton/210502_205734/0000'], 'data', 'SinglePhoton', '2017', 'F', '1', '1', '1'], '2017_D_SinglePhoton': [['rgoldouz/ExitedTopSamplesDataJan2021/SinglePhoton/crab_2017_D_SinglePhoton/210502_205653/0000'], 'data', 'SinglePhoton', '2017', 'D', '1', '1', '1'], '2017_E_SinglePhoton': [['rgoldouz/ExitedTopSamplesDataJan2021/SinglePhoton/crab_2017_E_SinglePhoton/210502_205638/0000'], 'data', 'SinglePhoton', '2017', 'E', '1', '1', '1'], '2017_C_SingleMuon': [['rgoldouz/ExitedTopSamplesDataJan2021/SingleMuon/crab_2017_C_SingleMuon/210502_205623/0000'], 'data', 'SingleMuon', '2017', 'C', '1', '1', '1'], '2017_C_SinglePhoton': [['rgoldouz/ExitedTopSamplesDataJan2021/SinglePhoton/crab_2017_C_SinglePhoton/210502_205720/0000'], 'data', 'SinglePhoton', '2017', 'C', '1', '1', '1'], '2017_E_SingleMuon': [['rgoldouz/ExitedTopSamplesDataJan2021/SingleMuon/crab_2017_E_SingleMuon/210502_205707/0000'], 'data', 'SingleMuon', '2017', 'E', '1', '1', '1'], '2017_B_SinglePhoton': [['rgoldouz/ExitedTopSamplesDataJan2021/SinglePhoton/crab_2017_B_SinglePhoton/210427_112656/0000'], 'data', 'SinglePhoton', '2017', 'B', '1', '1', '1'], '2017_D_SingleMuon': [['rgoldouz/ExitedTopSamplesDataJan2021/SingleMuon/crab_2017_D_SingleMuon/210502_205748/0000'], 'data', 'SingleMuon', '2017', 'D', '1', '1', '1'], '2017_F_SingleMuon': [['rgoldouz/ExitedTopSamplesDataJan2021/SingleMuon/crab_2017_F_SingleMuon/210502_205802/0000', 'rgoldouz/ExitedTopSamplesDataJan2021/SingleMuon/crab_2017_F_SingleMuon/210502_205802/0001'], 'data', 'SingleMuon', '2017', 'F', '1', '1', '1']}
