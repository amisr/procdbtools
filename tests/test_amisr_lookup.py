# test_amisr_lookup.py
# basic examples/tests for amisr_lookup.py

import datetime as dt
from procdbtools.amisr_lookup import AMISR_lookup

starttime = dt.datetime(2018,11,1)
endtime = dt.datetime(2018,12,1)

dbpath = '/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels'
amisrdb = AMISR_lookup('PFISR', db_path=dbpath)
experiments = amisrdb.find_experiments(starttime, endtime)
for exp in experiments:
    path = amisrdb.experiment_path(exp)
    print(path)

    filename = amisrdb.select_vvels_datafile(exp, pulse='lp')
    print(filename)
#    filename = amisrdb.select_vvels_datafile(exp, pulse='lp', integration='5min', post_integrate=True)
#    print(filename)



exp_nums = amisrdb.experiment_number(starttime, endtime)
print(exp_nums)

