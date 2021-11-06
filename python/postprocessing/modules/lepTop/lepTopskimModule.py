from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class lepTopskimModule(Module):
    def __init__(self):
        self.el9FiltTTH = lambda x: (x.pt>9 and x.mvaFall17V2noIso_WPL)
        self.el14FiltTTH = lambda x: (x.pt>14 and x.mvaFall17V2noIso_WPL)
        self.el24FiltTTH = lambda x: (x.pt>24 and x.mvaFall17V2noIso_WPL)
        self.el14FiltTT = lambda x: (x.pt>14 and x.cutBased > 3)
        self.el24FiltTT = lambda x: (x.pt>24 and x.cutBased > 3)

        self.mu9Filt = lambda x: (x.pt>9 and x.isGlobal)
        self.mu14Filt = lambda x: (x.pt>14 and x.isGlobal)
        self.mu24Filt = lambda x: (x.pt>24 and x.isGlobal)

        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        acceptEvent = False

        electrons9TTH = [x for x in filter(self.el9FiltTTH, Collection(event,"Electron"))]
        electrons14TTH = [x for x in filter(self.el14FiltTTH, Collection(event,"Electron"))]
        electrons24TTH = [x for x in filter(self.el24FiltTTH, Collection(event,"Electron"))]

        electrons14TT = [x for x in filter(self.el14FiltTT, Collection(event,"Electron"))]
        electrons24TT = [x for x in filter(self.el24FiltTT, Collection(event,"Electron"))]

        muons9     = [x for x in filter(self.mu9Filt, Collection(event,"Muon"    ))]
        muons14     = [x for x in filter(self.mu14Filt, Collection(event,"Muon"    ))]
        muons24     = [x for x in filter(self.mu24Filt, Collection(event,"Muon"    ))]

        TTH =  False
        TT = False
        if len(electrons9TTH)+len(muons9)>= 3 and len(electrons14TTH)+len(muons14)>= 2 and len(electrons24TTH)+len(muons24)>=1:
            TTH = True
        if len(electrons14TTH)+len(muons14)>= 2 and len(electrons24TTH)+len(muons24)>=1:
            TTH = True
        if len(electrons14TT)+len(muons14)>= 2 and len(electrons24TT)+len(muons24)>=1:
            TT = True
        if (TT or TTH):
            acceptEvent = True

        return acceptEvent

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
lepTopskimModuleConstr = lambda: lepTopskimModule()
