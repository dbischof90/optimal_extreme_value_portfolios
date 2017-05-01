
from models.common.basePortfolio import PortfolioModel
import scipy.optimize as opt
import numpy as np


class SurrogateMixPortfolio(PortfolioModel):

    def __init__(self, parameter, hiddenInfo):
        PortfolioModel.__init__(self, parameter=parameter, hiddenInfo=hiddenInfo)


    def __implicitFunction(self, x, weights, level):
        if self.hiddenInfo.FIRSTORDER:
            return np.inner(weights ** self.para.IND_REG, self.hiddenInfo.SCALES['first']) \
                   / (x ** self.para.IND_REG) - level
        else:
            if self.hiddenInfo.SINGLEFACTOR:
                return np.inner([w ** self.para.IND_REG for w in weights], self.hiddenInfo.SCALES['first']) / (x ** self.para.IND_REG * self.para.NUM_OF_ASSETS) + np.inner(weights, self.hiddenInfo.SCALES['second']) ** self.para.IND_HIDDEN / (x ** self.para.IND_HIDDEN) - 1 + level/100
            else:
                print('Not implemented!')
                return 0


    def calculateVaR(self, weights, level, start):
        result = opt.root(self.__implicitFunction, x0=start, args=(weights, level))
        return result.x[0]


    def calculateES(self, weights, level, start):
        VaR = self.calculateVaR(weights, level, start)
        return 100/(100 - level) * ( (sum([w ** self.para.IND_REG for w in weights]) * self.para.IND_REG)/(self.para.NUM_OF_ASSETS * (self.para.IND_REG - 1) * VaR ** (self.para.IND_REG - 1)) + self.para.IND_HIDDEN * np.inner(weights, self.hiddenInfo.SCALES['second']) ** self.para.IND_HIDDEN / ((self.para.IND_HIDDEN - 1) * VaR ** (self.para.IND_HIDDEN - 1)))