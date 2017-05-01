
import numpy as np
import scipy.optimize as opt

class PortfolioModel(object):
    def __init__(self, parameter, hiddenInfo):
        self.para = parameter
        self.optimalPortfolio = [s / sum(hiddenInfo.SCALES["second"]) for s in hiddenInfo.SCALES["second"]]
        self.hiddenInfo = hiddenInfo
        self.goodGuess = dict(typical = parameter.TYPICAL,
                              cubeSize = 0.1,
                              start = [s / sum(hiddenInfo.SCALES["second"]) for s in hiddenInfo.SCALES["second"]],
                              boundsLower = np.zeros(parameter.NUM_OF_ASSETS),
                              boundsUpper = np.ones(parameter.NUM_OF_ASSETS))
        self.initial = {"parameter": parameter, "hiddenInfo": hiddenInfo}

    def resetParameter(self):
        self.para = self.initial["parameter"]
        self.optimalPortfolio = [s / sum(self.initial["hiddenInfo"].SCALES["second"]) for s in self.initial["hiddenInfo"].SCALES["second"]]
        self.hiddenInfo = self.initial["hiddenInfo"]
        self.goodGuess = dict(typical = self.initial["parameter"].TYPICAL,
                              cubeSize = 0.1,
                              start = [s / sum(self.initial["hiddenInfo"].SCALES["second"]) for s in self.initial["hiddenInfo"].SCALES["second"]],
                              boundsLower = np.zeros(self.initial["parameter"].NUM_OF_ASSETS),
                              boundsUpper = np.ones(self.initial["parameter"].NUM_OF_ASSETS))

    def calculateVaR(self, *args):
        pass

    def calculateES(self, *args):
        pass

    def calculateVariance(self, *args):
        pass

    def updateOptimizationConstraints(self, center=None):
        if center is None:
            center = self.optimalPortfolio.x
        self.goodGuess["start"] = np.array(center)
        self.goodGuess["boundsLower"] = np.maximum(self.goodGuess["start"] - self.goodGuess["cubeSize"], np.zeros(self.para.NUM_OF_ASSETS))
        self.goodGuess["boundsUpper"] = np.minimum(self.goodGuess["start"] + self.goodGuess["cubeSize"], np.ones(self.para.NUM_OF_ASSETS))

    # noinspection PyTypeChecker
    def getOptimalPortfolio(self, measure, level, portSpecificValue, optimizeConstraints = True, getOutput = False):
        if measure == 'VaR':
            objectiveFunction = self.calculateVaR
        elif measure == 'ES':
            objectiveFunction = self.calculateES
        elif measure == 'Variance':
            objectiveFunction = self.calculateVariance
        else:
            print("Wrong objective function in optimizer!")
            return False

        optimalPortfolio = opt.minimize(
            objectiveFunction, x0=self.goodGuess["start"], args=(level, portSpecificValue),
            constraints=dict(type='eq',
                             fun=lambda x: np.dot(np.ones(self.para.NUM_OF_ASSETS), x) - 1),
            bounds=tuple([(l, u) for l, u in zip(self.goodGuess["boundsLower"], self.goodGuess["boundsUpper"])]))

        if getOutput:
            return optimalPortfolio

        else:
            self.optimalPortfolio = optimalPortfolio
            self.goodGuess["typical"] = (self.optimalPortfolio.fun, level)
            if optimizeConstraints:
                self.updateOptimizationConstraints()
            return True
