# create_file_list_LG.py
# Create a list of processed RISR filenames for L. Goodwin
# One file per experiment
# Time resolution closest to 1 min
# Check that file actually exist

import datetime as dt
from amisr_lookup import AMISR_lookup


risrdb = AMISR_lookup('RISR-N')

# experiments = risrdb.find_experiments(dt.datetime(2009,1,1), dt.datetime(2023,1,1))
experiments = risrdb.find_experiments(dt.datetime(2017,11,1), dt.datetime(2017,12,1))

with open('RISRN_file_list.txt', 'w') as outfile:

    for e in experiments:
        print(e['exp_num'])
        ep = risrdb.experiment_path(e)
        filename = risrdb.select_experiment_file(ep, check_exists=True)
        if filename:
            outfile.write(filename.name+'\n')
