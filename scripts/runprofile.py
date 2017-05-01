
from datetime import datetime, timedelta
from time import time
from numba import jit
from models.analytical import SurrogateMixPortfolio
from models.common.structs import HiddenRegularInformation, ParameterForPortfolio
from models.empirical import EmpiricalPortfolio


@jit
def runProfile(profile):
    print("Profile \'" + profile.NAME + "\' launched at " + str((datetime.now()).replace(microsecond=0))[11:] + ".")
    startTotal = time()
    infoStruct = HiddenRegularInformation(profile)
    paraStruct = ParameterForPortfolio(profile)

    empiricalPortfolio = EmpiricalPortfolio(paraStruct, infoStruct, profile.SAMPLESIZE)
    analyticalPortfolio = SurrogateMixPortfolio(paraStruct, infoStruct)

    results = {}

    for measure in profile.RISKMEASURES:
        start = time()
        empiricalPortfolio.resetParameter()
        analyticalPortfolio.resetParameter()
        analyticalPortfolio.goodGuess["cubeSize"] = 0.05
        empiricalPortfolio.goodGuess["cubeSize"] = 0.15
        analyticalOptimalPortfolios = []
        empiricalOptimalPortfolios = []
        recalCountAna = []
        recalCountEmp = []
        noPortfolio = []
        results[measure] = {}
        profile.RESULTINFORMATION[measure] = {}
        for step in range(profile.RES + profile.BURNIN):
            level = profile.STARTVAR + 10 * (step - profile.BURNIN) / profile.RES
            empiricalPortfolio.getOptimalPortfolio(measure, level, profile.SET)
            analyticalPortfolio.getOptimalPortfolio(measure, level, analyticalPortfolio.goodGuess["typical"][0])
            if analyticalPortfolio.optimalPortfolio.fun < 0 or \
                    (len(analyticalOptimalPortfolios) > 0 and analyticalPortfolio.optimalPortfolio.fun < analyticalOptimalPortfolios[-1].fun):
                surrogateStart = empiricalPortfolio.optimalPortfolio.fun * (analyticalPortfolio.para.IND_REG - 1)/analyticalPortfolio.para.IND_REG
                analyticalPortfolio.updateOptimizationConstraints(analyticalOptimalPortfolios[-1].x)
                analyticalPortfolio.getOptimalPortfolio(measure, level, surrogateStart)
                recalCountAna.append(level)
                if analyticalPortfolio.optimalPortfolio.fun < 0 or \
                        (len(analyticalOptimalPortfolios) > 0 and analyticalPortfolio.optimalPortfolio.fun < analyticalOptimalPortfolios[-1].fun):
                    print("Warning: Process \'" + profile.NAME + "\' needs empirical approximation of start value at level " + str(round(level, 2)) +
                    ". Calculate empirical surrogate approximation and restart step.")
                    recalCountEmp.append(level)
                    surrogateStart = empiricalPortfolio.getOptimalPortfolio("VaR", level, "mixed", getOutput=True)
                    analyticalPortfolio.updateOptimizationConstraints(surrogateStart.x)
                    analyticalPortfolio.getOptimalPortfolio(measure, level, surrogateStart.fun)
                    if analyticalPortfolio.optimalPortfolio.fun < 0 or \
                            (len(analyticalOptimalPortfolios) > 0 and analyticalPortfolio.optimalPortfolio.fun < analyticalOptimalPortfolios[-1].fun):
                        print("Warning: Process \'" + profile.NAME + "\' failed to find optimal value at level " + str(round(level, 2)) + ".")
                        noPortfolio.append(level)

            if step >= profile.BURNIN:
                analyticalOptimalPortfolios.append(analyticalPortfolio.optimalPortfolio)
                empiricalOptimalPortfolios.append(empiricalPortfolio.optimalPortfolio)
            if not (step + 1) % round((profile.RES + profile.BURNIN)/5):
                remainingSeconds = (time() - start) * (profile.RES + profile.BURNIN - step)/ step
                print("Progress notification: Process \'" + profile.NAME + "\' has completed roughly " +
                      str(round(step * 5/(profile.RES + profile.BURNIN))) + "/5 of its steps for " + measure +". Estimated end time: " +
                      str((datetime.now() + timedelta(seconds=remainingSeconds)).replace(microsecond=0))[11:])

        results[measure]["analytical"] = analyticalOptimalPortfolios
        results[measure]["empirical"] = empiricalOptimalPortfolios
        profile.RESULTINFORMATION[measure]["restart_analytical"] = recalCountAna
        profile.RESULTINFORMATION[measure]["restart_empirical"] = recalCountEmp
        profile.RESULTINFORMATION[measure]["no_portfolio"] = noPortfolio
        profile.RESULTINFORMATION[measure]["average_speed"] = (profile.RES + profile.BURNIN)/(time() - startTotal)

    print("Profile \'" + profile.NAME + "\' completed. Total time: " + str(round(time() - startTotal, 2)) + " seconds.")
    return dict(data=results, profile=profile)
