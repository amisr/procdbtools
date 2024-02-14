# amisr_lookup.py
# Look up the experiment an AMISR radar was running in durring a particular period,
#   including mode/experiment information.
# Requires sqlalchemy and the appropriate AMISR SQL database

# Change name to datasearchtools? - amisr_find_experiment
# combine both raw and processed tools
# Capable to check that file exists on NAS AND/OR file available to download
# Given this time interval, what experiment was running
#
# Cron to update data every hour - currently in Pablo's workspace

####################################################################
#  UPDATING DATABASE FILE
# To update the database file (amisrdb), copy it from io2 at the
# following file path:
#
# /opt/websites/database/calendar/isr_database/amisrdb
#
#####################################################################


import datetime as dt
import sqlalchemy
import pathlib
import re
from importlib.resources import files

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

#from .dbmodels import Site, Experiment, RadarMode
from .procdbmodels import *
from .manage_database import procdb_file as default_procdb_file

# Add command line programs to:
# 1. Given time, print experiment number and mode
# 2. Create file list

# Add some kind of functionality/instructions to update database file


class AMISR_lookup(object):
#    # OPTIONS:
#    1. Return just experiment number
#    2. Return experiment number and other information (ie, mode)
#    3. Return path to experiment
#    4. Return path to specific file
#    5. Return all of the above??

    def __init__(self, radar, procdb_file=None, db_path=None):

        self.radar = radar

        if not procdb_file:
            procdb_file = default_procdb_file

        engine = create_engine("sqlite:///{}".format(procdb_file))
        Session = sessionmaker(bind=engine)
        self.session = Session()

        if db_path:
            self.db_path = db_path
        else:
            self.db_path = '/Volumes/AMISR_PROCESSED/processed_data'
        # Check that this path exists and do something if not valid??



    def find_experiments(self, starttime, endtime):
        """
        Return list of all experiments between two times
        """

        # Get instrument ID number
        inst = self.session.query(ProcdbInstrument).filter(ProcdbInstrument.abbr==self.radar).one()
        inst_id = inst.id

        # Find experiment by start/end times and radar id
        conditions = sqlalchemy.and_(ProcdbExperiment.inst_id==inst_id,
                                     ProcdbExperiment.end_time>starttime,
                                     ProcdbExperiment.start_time<endtime)
        filt_exp = self.session.query(ProcdbExperiment).filter(conditions).all()

        return filt_exp

    def find_experiment(self, time):
        """
        Return experiment run at a particular time
        """

        # Get instrument ID number
        inst = self.session.query(ProcdbInstrument).filter(ProcdbInstrument.abbr==self.radar).one()
        inst_id = inst.id

        # Find experiment by start/end times and radar id
        conditions = sqlalchemy.and_(ProcdbExperiment.inst_id==inst_id,
                                     ProcdbExperiment.end_time>time,
                                     ProcdbExperiment.start_time<=time)
        filt_exp = self.session.query(ProcdbExperiment).filter(conditions).one()

        return filt_exp

    def experiment_number(self, starttime, endtime):
        """
        Return just a list of experiment numbers
        """
        exp_list = self.find_experiments(starttime, endtime)
        exp_num = [exp.experiment for exp in exp_list]
        return exp_num

    def get_mode(self, exp):
        mode_id = exp.type_id
        mode = self.session.query(ProcdbExperimentType).filter(ProcdbExperimentType.id==mode_id).one()
        return mode.label


    def experiment_path(self, exp):
        """
        Return the full path to a given experiment directory
        """

        mode = self.get_mode(exp)

        expdir = pathlib.Path(self.db_path, self.radar, f'{exp.start_year:04}', f'{exp.start_month:02}', mode, exp.experiment)

        # check if path exists before returning
        if not expdir.exists():
            expdir = expdir.with_name(exp.experiment+'.done')

        if expdir.exists():
            return expdir
        else:
            return None



    def select_datafile(self, exp, pulse=None, integration=None, cal=None, check_exists=False):

        # Get path to experiment
        experiment_path = self.experiment_path(exp)
        if not experiment_path:
            return None

        datafiles = [f.name for f in experiment_path.glob('*.h5')]

        # Reduce set to only files with the correct pulse
        datafiles = [df for df in datafiles if df.startswith(f'{exp.experiment}_{pulse}')]

        if not datafiles:
            return None

        # If no time resolution specified, find file with shortest integration time
        if not integration:
            int_times = list()
            for df in datafiles:
                time_re = re.search(r'\d+min', df)
                if time_re:
                    int_times.append(int(time_re.group()[:-3]))
                else:
                    continue
            timeres = min(int_times)
            integration = f'{timeres}min'
        # Select files with specified integration time
        datafiles = [df for df in datafiles if df.startswith(f'{exp.experiment}_{pulse}_{integration}-')]

        # If cal not specified, use deault ordering
        if not cal:
            if any([df.endswith('min-fitcal.h5') for df in datafiles]):
                cal = 'fitcal'
            elif any([df.endswith('min-cal.h5') for df in datafiles]):
                cal = 'cal'
            else:
                cal = ''
        # Select file with specified calibration
        datafiles = [df for df in datafiles if df.startswith(f'{exp.experiment}_{pulse}_{integration}-{cal}')]
 
        try:
            datafile = datafiles[0]
        except IndexError:
            return None

        filename = experiment_path.joinpath(datafile)

        if check_exists:
            if not filename.is_file():
                return None

        return filename


    def select_vvels_datafile(self, exp, pulse=None, integration=None, post_integrate=False, check_exists=False):

        # Get path to experiment
        experiment_path = self.experiment_path(exp)
        if not experiment_path:
            return None
        experiment_path = experiment_path.joinpath('derivedParams/new_vvels')

        datafiles = [f.name for f in experiment_path.glob('*.h5')]

        # Reduce set to only files with the correct pulse
        datafiles = [df for df in datafiles if df.startswith(f'{exp.experiment}_{pulse}')]

        if not datafiles:
            return None

        # If no time resolution specified, find file with shortest integration time
        if not integration:
            int_times = list()
            for df in datafiles:
                time_re = re.search(r'\d+min', df)
                if time_re:
                    int_times.append(int(time_re.group()[:-3]))
                else:
                    continue
            timeres = min(int_times)
            integration = f'{timeres}min'

        # Select files with specified integration time
        if not post_integrate:
            datafiles = [df for df in datafiles if df.startswith(f'{exp.experiment}_{pulse}_{integration}-')]
        else:
            datafiles = [df for df in datafiles if df.endswith(f'-{integration}.h5')]


        try:
            datafile = datafiles[0]
        except IndexError:
            return None

        filename = experiment_path.joinpath(datafile)

        if check_exists:
            if not filename.is_file():
                return None

        return filename




    def site_coords(self):
        radar_shortname = self.radar.replace('-','').lower()
        site = self.session.query(db.Site).filter(db.Site.shortname==radar_shortname).one()
        return site
    
    
