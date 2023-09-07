# test_amisr_lookup.py
# basic examples/tests for amisr_lookup.py

import datetime as dt
from procdbtools.amisr_lookup import AMISR_lookup

starttime = dt.datetime(2017,11,1)
endtime = dt.datetime(2017,12,1)

amisrdb = AMISR_lookup('PFISR')

experiments = amisrdb.find_experiments(starttime, endtime)
for exp in experiments:
    path = amisrdb.experiment_path(exp)
    print(path)

    filename = amisrdb.select_datafile(exp, pulse='lp', integration='5min')
    print(filename)


exp_nums = amisrdb.experiment_number(starttime, endtime)
print(exp_nums)

