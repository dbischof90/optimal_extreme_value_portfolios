
from scripts.runprofile import runProfile, giveInfos
from models.common.structs import Profile
from multiprocessing import Pool

profile1 = Profile()
profile1.SAMPLESIZE = 1000000
profile1.NAME = "Full, standard"
profile1.RES = 150
profile1.RISKMEASURES = ["ES", "VaR"]
profile1.SET = "full"
profile1.BURNIN = 50

profile2 = Profile()
profile2.SAMPLESIZE = 6000000
profile2.NAME = "Ten assets"
profile2.RES = 500
profile2.RISKMEASURES = ["ES", "VaR"]
profile2.SET = "full"
profile2.BURNIN = 50
profile2.SCALES = {'first': [1,1,1,1,1,1,1,1,1,1], 'second': [1.3,0.8,1,0.6, 1.1, 1.9, 0.9, 1.1, 1.4, 1.5]}


jobs = [profile1, profile2]
workers = min(2, len(jobs))
p = Pool(workers)

giveInfos(jobs, workers)
res = p.map(runProfile, jobs)

#x = runProfile(profile2)

print("done")
