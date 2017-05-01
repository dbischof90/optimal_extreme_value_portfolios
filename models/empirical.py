
from models.common.basePortfolio import PortfolioModel
import numpy as np

class EmpiricalPortfolio(PortfolioModel):

    def __init__(self, parameter, hiddenInfo, sampleSize):
        PortfolioModel.__init__(self, parameter=parameter, hiddenInfo=hiddenInfo)
        self.data = {}
        self.sampleSize = sampleSize
        self.data['full'] = self.__createDataSet('full')
        self.data['mixed'] = self.__createDataSet('mixed')


    def __createDataSet(self, type):

        betas = np.array(self.hiddenInfo.SCALES['second'])
        betas.shape = (self.para.NUM_OF_ASSETS, 1)

        if type == 'full':
            X = np.random.pareto(self.para.IND_REG, size=(self.para.NUM_OF_ASSETS, self.sampleSize)) + 1
            bY = np.multiply(np.tile(np.random.pareto(self.para.IND_HIDDEN, size=(1, self.sampleSize)) + 1, (self.para.NUM_OF_ASSETS, 1)), np.tile(betas, (1, self.sampleSize)))
            return X + bY

        elif type == 'mixed':
            B = np.tile(np.random.binomial(1, 0.5, size=(1 ,self.sampleSize)), (self.para.NUM_OF_ASSETS, 1))
            B_fO =  np.random.multinomial(1, [1/self.para.NUM_OF_ASSETS]*self.para.NUM_OF_ASSETS, size=self.sampleSize).T
            X = np.random.pareto(self.para.IND_REG, size=(self.para.NUM_OF_ASSETS, self.sampleSize)) + 1
            bV = np.multiply(np.tile(np.random.pareto(self.para.IND_HIDDEN, size=(1, self.sampleSize)) + 1, (self.para.NUM_OF_ASSETS, 1)), np.tile(betas, (1, self.sampleSize)))
            return 2 ** (1/self.para.IND_REG) * np.multiply(np.multiply(B, B_fO), X) + 2 ** (1/self.para.IND_HIDDEN) * np.multiply(1 - B, bV)


    def calculateVaR(self, weights, level, type):
        return np.percentile(np.dot(self.data[type].T, weights), level)


    def calculateES(self, weights, level, type):
        sortedValues = np.sort(np.dot(self.data[type].T, weights))
        return sum(sortedValues[self.sampleSize - round(self.sampleSize * (100 - level)/100):])/(round(self.sampleSize * (100 - level)/100) + 1)

    def calculateVariance(self, weights, level, type):
        return np.var(np.dot(self.data[type].T, weights))