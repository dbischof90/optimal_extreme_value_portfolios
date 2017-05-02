from multiprocessing import Pool

from models.common.structs import Profile
from scripts.analyze import giveInfos
from scripts.analyze import plotPortfolioWeights
from scripts.runprofile import runProfile

profile1 = Profile()
profile1.SAMPLESIZE = 500000
profile1.NAME = "Two assets, full"
profile1.RES = 500
profile1.RISKMEASURES = ["ES", "VaR"]
profile1.SET = "full"
profile1.BURNIN = 20
profile1.SCALES = {'first': [1, 1], 'second': [1.3, 0.8]}

profile2 = Profile()
profile2.SAMPLESIZE = 500000
profile2.NAME = "Two assets, mixed"
profile2.RES = 500
profile2.RISKMEASURES = ["ES", "VaR"]
profile2.SET = "mixed"
profile2.BURNIN = 20
profile2.SCALES = {'first': [1, 1], 'second': [1.3, 0.8]}

jobs = [profile1, profile2]
workers = min(2, len(jobs))
p = Pool(workers)

giveInfos(jobs, workers)
res = p.map(runProfile, jobs)
plotPortfolioWeights(res)

print("Analysis complete.")
