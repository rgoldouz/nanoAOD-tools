import datetime
import os
import os.path
import sys
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow, Dataset,ParentDataset
sys.path.append(os.path.abspath("."))
import Files_2017

SAMPLES = {}
mc_2017 = True
data_2017 = True

cmsswbase = os.environ['CMSSW_BASE']
timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

username = "rgoldouz"

production_tag = "NanoAodPostProcessingUL"            # For 'full_production' setup
UL_YEAR = 'UL17'
out_ver = "v1"   # The version index for the OUTPUT directory

if UL_YEAR=='UL17':
    SAMPLES.update(Files_2017.mc2017_samples)
    SAMPLES.update(Files_2017.data2017_samples) 

# Only run over lhe steps from specific processes/coeffs/runs
process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []  # (i.e. MG starting points)

master_label = 'T3_NanoAodPostProcessingULhadoop_{tstamp}'.format(tstamp=timestamp_tag)


input_path   = "/store/user/"
output_path  = "/store/user/$USER/%s/%s/%s" % (production_tag,UL_YEAR,out_ver)
workdir_path = "/tmpscratch/users/$USER/FullProduction/Hadoop/%s/%s/%s" % (production_tag,UL_YEAR,out_ver)
plotdir_path = "~/www/lobster/FullProduction/Hadoop/%s/%s/%s" % (production_tag,UL_YEAR,out_ver)


storage = StorageConfiguration(
    input = [
        "root://deepthought.crc.nd.edu/" + input_path,  # Note the extra slash after the hostname!
        "hdfs://eddie.crc.nd.edu:19000"  + input_path,
        "gsiftp://T3_US_NotreDame"       + input_path,
        "srm://T3_US_NotreDame"          + input_path,
    ],
    output=[
        "hdfs://eddie.crc.nd.edu:19000"  + output_path,
        "root://deepthought.crc.nd.edu/" + output_path, # Note the extra slash after the hostname!
        "gsiftp://T3_US_NotreDame"       + output_path,
        "srm://T3_US_NotreDame"          + output_path,
        "file:///hadoop"                 + output_path,
    ],
    disable_input_streaming=True,
)

#################################################################
# Worker Res.:
#   Cores:  12    | 4
#   Memory: 16000 | 8000
#   Disk:   13000 | 6500
#################################################################
gs_resources = Category(
    name='gs',
    cores=1,
    memory=1200,
    disk=2900
)
#################################################################
# Note, since we need to use data files in PhysicsTools/NanoAODTools/, we need to use a sandbox from the same CMSSW with all it's contents,
# tar cjvf sandbox-CMSSW_10_2_18-slc7_amd64_gcc700_3Nov-a6a7ccc.tar.bz2 CMSSW_10_2_18
wf = []
for key, value in SAMPLES.items():
    if value[5]=='DAS':
        continue
    print key
    Analysis = Workflow(
        label=key,
        sandbox=cmssw.Sandbox(release='/afs/crc.nd.edu/user/r/rgoldouz/Ntupleproducer/NanoAOD/CMSSW_10_2_18', include=['PhysicsTools/NanoAODTools']),
        globaltag=False,
        command='python Lobster_postproc.py .' +' @inputfiles' + ' --DataProcessing=' + value[1] + ' --year=' + value[2] + ' --run=' +  value[3] + ' --json=' + value[4],
        extra_inputs=['Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt', 'Lobster_postproc.py'],
        outputs=['tree.root'],
        dataset=Dataset(files=value[0][0],patterns=["*.root"],files_per_task =1),
        category=gs_resources
    )
    wf.append(Analysis)

config = Config(
    label=master_label,
    workdir=workdir_path,
    plotdir=plotdir_path,
    storage=storage,
    workflows=wf,
    advanced=AdvancedOptions(
        bad_exit_codes=[127, 160],
        log_level=1,
        payload=10,
        dashboard = False,
        xrootd_servers=['ndcms.crc.nd.edu',
                       'cmsxrootd.fnal.gov',
                       'deepthought.crc.nd.edu'
        ],
    )
)

