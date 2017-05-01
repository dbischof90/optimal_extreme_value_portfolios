
from matplotlib import pyplot as plt
from tabulate import tabulate
from projectRoot import ROOT_DIR
import pickle

PLOT_DIR = ROOT_DIR + "/results"
DATA_DIR = ROOT_DIR + "/data"

def plotPortfolioWeights(results):
    for simulation in results:
        for measure in simulation["data"].keys():
            fig = plt.figure()
            fig.suptitle('Portfolio weights for ' + measure + '-optimal portfolios', fontsize=14, fontweight='bold')
            ax = fig.add_subplot(111)
            ax.set_title('Profile: ' + str(simulation["profile"].NAME) +
                         ', Regular tail index: ' + str(simulation["profile"].IND_REG) +
                         ', Hidden tail index: ' + str(simulation["profile"].IND_HIDDEN))
            ax.plot([e.x for e in simulation["data"][measure]["analytical"]])
            ax.plot([e.x for e in simulation["data"][measure]["empirical"]])
            ax.set_xticks([x * simulation["profile"].RES / 10 for x in range(11)])
            ax.set_xticklabels([simulation["profile"].STARTVAR + x for x in range(11)])


def giveInfos(listOfProfiles, numWorkers):

    infoString = []
    for profile in listOfProfiles:
        infoString.append(tabulate([["Name:", profile.NAME],
                      ["Steps to calculate:", profile.RES],
                      ["Sample size:", profile.SAMPLESIZE],
                      ["Used risk measures:", ', '.join(profile.RISKMEASURES)]], tablefmt="simple"))
        infoString.append('\n')

    if numWorkers > 1:
        numProcesses = "Jobs splitted to " + str(numWorkers) + " cores"
    else:
        numProcesses = "Single-core execution"
    print('New profiles in queue:\n' + ''.join(infoString) +
          '\nTotal number: ' + str(len(listOfProfiles)) +
          '\n' + numProcesses + '\n')