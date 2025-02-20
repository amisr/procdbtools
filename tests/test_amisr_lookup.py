# test_amisr_lookup.py
# basic examples/tests for amisr_lookup.py

import pytest
from pathlib import Path
import datetime as dt
from procdbtools.amisr_lookup import AMISR_lookup

##starttime = dt.datetime(2013,4,8)
##endtime = dt.datetime(2013,4,9)
#starttime = dt.datetime(2014,3,8)
#endtime = dt.datetime(2014,3,9)
#
##dbpath = '/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels'
##dbpath = '/Volumes/AMISR_PROCESSED/processed_data'
#amisrdb = AMISR_lookup('PFISR')
#experiments = amisrdb.find_experiments(starttime, endtime, no_duplicates=False)
#for exp in experiments:
#    print(exp.name)
#    #path = amisrdb.experiment_path(exp)
#    ##print(path)
#
#    #filename = amisrdb.select_datafile(exp, pulse='lp', integration='5min')
#    ##filename = amisrdb.select_vvels_datafile(exp, pulse='lp', integration='5min', post_integrate=True)
#    #print(filename)
##    filename = amisrdb.select_vvels_datafile(exp, pulse='lp', integration='5min', post_integrate=True)
##    print(filename)


###################
## UNIT TESTS
###################

@pytest.fixture
def pfisrdb_processed():
    dbpath = '/Volumes/AMISR_PROCESSED/processed_data'
    pfisrdb = AMISR_lookup('PFISR', db_path=dbpath)
    return pfisrdb

@pytest.fixture
def pfisrdb_vvels():
    dbpath = '/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels'
    pfisrdb = AMISR_lookup('PFISR', db_path=dbpath)
    return pfisrdb


def test_find_experiments(pfisrdb_processed):
    starttime = dt.datetime(2013,4,8)
    endtime = dt.datetime(2013,4,9)
    exp_list = pfisrdb_processed.find_experiments(starttime, endtime)
    exp_num = [exp.name for exp in exp_list]
    assert exp_num == ['20130406.001','20130408.001','20130408.002']
    
def test_find_experiments_concat(pfisrdb_processed):
    starttime = dt.datetime(2014,3,8)
    endtime = dt.datetime(2014,3,9)
    exp_list = pfisrdb_processed.find_experiments(starttime, endtime)
    exp_num = [exp.name for exp in exp_list]
    assert exp_num == ['20140308.001', '20140308.002', '20140308.004', '20140308.005', '20140308.007', '20140308.009', '20140308.011', '20140308.012', '20140308.014', '20140308.015']

def test_find_experiments_concat_with_duplicates(pfisrdb_processed):
    starttime = dt.datetime(2014,3,8)
    endtime = dt.datetime(2014,3,9)
    exp_list = pfisrdb_processed.find_experiments(starttime, endtime, no_duplicates=False)
    exp_num = [exp.name for exp in exp_list]
    assert exp_num == ['20140308.001', '20140308.002', '20140308.003', '20140308.004', '20140308.005', '20140308.006', '20140308.007', '20140308.008', '20140308.009', '20140308.011', '20140308.012', '20140308.013', '20140308.014', '20140308.015', '20140308.016']

def test_find_experiment(pfisrdb_processed):
    time = dt.datetime(2013,4,8,11,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    assert exp.name == '20130408.001'

def test_get_mode(pfisrdb_processed):
    time = dt.datetime(2013,4,8,11,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    mode = pfisrdb_processed.get_mode(exp)
    assert mode == 'Themis36'

def test_get_experiment_number_standard(pfisrdb_processed):
    time = dt.datetime(2013,3,28,11,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    exp_num = pfisrdb_processed.get_experiment_number(exp)
    assert exp_num == '20130327.001'

def test_get_experiment_number_concat(pfisrdb_processed):
    time = dt.datetime(2013,3,28,18,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    exp_num = pfisrdb_processed.get_experiment_number(exp)
    assert exp_num == '20130327.001'


def test_experiment_path(pfisrdb_processed):
    time = dt.datetime(2019,1,23,12,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    path = pfisrdb_processed.experiment_path(exp)
    assert path == Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2019/01/Themis36/20190123.003')

def test_experiment_path_done(pfisrdb_processed):
    time = dt.datetime(2014,9,22,12,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    path = pfisrdb_processed.experiment_path(exp)
    assert path == Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2014/09/WorldDay35/20140922.002.done')

def test_select_datafile_ac(pfisrdb_processed):
    time = dt.datetime(2014,1,11,2,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    filename = pfisrdb_processed.select_datafile(exp, pulse='ac', integration='1min', cal='fitcal')
    assert filename == Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2014/01/Themis36/20140111.001/20140111.001_ac_1min-fitcal.h5')

def test_select_datafile_lp(pfisrdb_processed):
    time = dt.datetime(2014,1,11,2,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    filename = pfisrdb_processed.select_datafile(exp, pulse='lp', integration='1min', cal='fitcal')
    assert filename == Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2014/01/Themis36/20140111.001/20140111.001_lp_1min-fitcal.h5')

def test_select_datafile_int(pfisrdb_processed):
    time = dt.datetime(2022,5,5,8,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    exp_dir = Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2022/05/Themis36/20220505.001')
    for it in ['1min', '3min', '5min', '10min', '15min', '20min']:
        filename = pfisrdb_processed.select_datafile(exp, pulse='lp', integration=it, cal='fitcal')
        assert filename == exp_dir.joinpath(f'20220505.001_lp_{it}-fitcal.h5')

def test_select_datafile_no_int(pfisrdb_processed):
    time = dt.datetime(2022,5,5,8,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    filename = pfisrdb_processed.select_datafile(exp, pulse='lp', cal='fitcal')
    assert filename == Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2022/05/Themis36/20220505.001/20220505.001_lp_1min-fitcal.h5')

def test_select_datafile_bad_int(pfisrdb_processed):
    time = dt.datetime(2022,5,5,8,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    filename = pfisrdb_processed.select_datafile(exp, pulse='lp', integration='4min', cal='fitcal')
    assert filename == None

def test_select_datafiles_fitcal(pfisrdb_processed):
    time = dt.datetime(2014,1,11,10,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    filename = pfisrdb_processed.select_datafile(exp, pulse='lp', integration='1min', cal='fitcal')
    assert filename == None

def test_select_datafiles_cal(pfisrdb_processed):
    time = dt.datetime(2014,1,11,10,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    filename = pfisrdb_processed.select_datafile(exp, pulse='lp', integration='1min', cal='cal')
    assert filename == Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2014/01/Themis36/20140111.003/20140111.003_lp_1min-cal.h5')

def test_select_datafiles_nocal(pfisrdb_processed):
    time = dt.datetime(2014,1,11,10,0,0)
    exp = pfisrdb_processed.find_experiment(time)
    filename = pfisrdb_processed.select_datafile(exp, pulse='lp', integration='1min')
    assert filename == Path('/Volumes/AMISR_PROCESSED/processed_data/PFISR/2014/01/Themis36/20140111.003/20140111.003_lp_1min-cal.h5')


# test_select_vvels_datafile
#   - integration specified
#   - integration not specified
#   - ac
#   - lp
#   - fitcal
#   - cal
#   - calibration not specified
#   - file does not exist
#   - post-integration
#   - no post-integration

def test_select_vvels_datafile_lp(pfisrdb_vvels):
    time = dt.datetime(2014,1,11,2,0,0)
    exp = pfisrdb_vvels.find_experiment(time)
    filename = pfisrdb_vvels.select_vvels_datafile(exp, pulse='lp', integration='1min', cal='fitcal')
    assert filename == Path('/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels/PFISR/2014/01/Themis36/20140111.001/derivedParams/new_vvels/20140111.001_lp_1min-fitcal-vvels_lat.h5')

def test_select_vvels_datafile_int(pfisrdb_vvels):
    time = dt.datetime(2022,5,5,8,0,0)
    exp = pfisrdb_vvels.find_experiment(time)
    exp_dir = Path('/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels/PFISR/2022/05/Themis36/20220505.001/derivedParams/new_vvels')
    for it in ['1min', '3min', '5min', '10min', '15min', '20min']:
        filename = pfisrdb_vvels.select_vvels_datafile(exp, pulse='lp', integration=it, cal='fitcal')
        assert filename == exp_dir.joinpath(f'20220505.001_lp_{it}-fitcal-vvels_lat.h5')

def test_select_vvels_datafile_no_int(pfisrdb_vvels):
    time = dt.datetime(2022,5,5,8,0,0)
    exp = pfisrdb_vvels.find_experiment(time)
    filename = pfisrdb_vvels.select_vvels_datafile(exp, pulse='lp', cal='fitcal')
    assert filename == Path('/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels/PFISR/2022/05/Themis36/20220505.001/derivedParams/new_vvels/20220505.001_lp_1min-fitcal-vvels_lat.h5')

def test_select_vvels_datafile_bad_int(pfisrdb_vvels):
    time = dt.datetime(2022,5,5,8,0,0)
    exp = pfisrdb_vvels.find_experiment(time)
    filename = pfisrdb_vvels.select_vvels_datafile(exp, pulse='lp', integration='4min', cal='fitcal')
    assert filename == None

def test_select_vvels_datafiles_fitcal(pfisrdb_vvels):
    time = dt.datetime(2014,1,11,10,0,0)
    exp = pfisrdb_vvels.find_experiment(time)
    filename = pfisrdb_vvels.select_vvels_datafile(exp, pulse='lp', integration='1min', cal='fitcal')
    assert filename == None

def test_select_vvels_datafiles_cal(pfisrdb_vvels):
    time = dt.datetime(2014,1,11,10,0,0)
    exp = pfisrdb_vvels.find_experiment(time)
    filename = pfisrdb_vvels.select_vvels_datafile(exp, pulse='lp', integration='1min', cal='cal')
    assert filename == Path('/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels/PFISR/2014/01/Themis36/20140111.003/derivedParams/new_vvels/20140111.003_lp_1min-cal-vvels_lat.h5')

def test_select_vvels_datafiles_nocal(pfisrdb_vvels):
    time = dt.datetime(2014,1,11,10,0,0)
    exp = pfisrdb_vvels.find_experiment(time)
    filename = pfisrdb_vvels.select_vvels_datafile(exp, pulse='lp', integration='1min')
    assert filename == Path('/Volumes/AMISR_SCRATCH/llamarche/AMISR_custom/new_vvels/PFISR/2014/01/Themis36/20140111.003/derivedParams/new_vvels/20140111.003_lp_1min-cal-vvels_lat.h5')

