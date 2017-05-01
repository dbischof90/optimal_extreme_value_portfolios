
class Profile(object):
    NAME = "Default"
    RES = 500
    BURNIN = 30
    SAMPLESIZE = 2000000
    STARTVAR = 90
    RISKMEASURES = ["VaR"]
    SET = "full"
    IND_REG = 2
    IND_HIDDEN = 3
    NUM_OF_ASSETS = 2
    TYPICAL = (4, 90)
    FIRSTORDER = False
    SINGLEFACTOR = True
    SCALES = {'first': [1, 1],
              'second': [1.3, 0.8]}
    RESULTINFORMATION = {}

class HiddenRegularInformation(object):
    def __init__(self, profile):
        self.FIRSTORDER = profile.FIRSTORDER
        self.SINGLEFACTOR = profile.SINGLEFACTOR
        self.SCALES = profile.SCALES

class ParameterForPortfolio(object):
    def __init__(self, profile):
        self.IND_REG = profile.IND_REG
        self.IND_HIDDEN = profile.IND_HIDDEN
        self.NUM_OF_ASSETS = len(profile.SCALES['first'])
        self.TYPICAL = profile.TYPICAL