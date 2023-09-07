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


import datetime as dt
import sqlalchemy
import pathlib
import re
from importlib_resources import files

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

from .dbmodels import Site, Experiment, RadarMode

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
            # Use package data instead? (eventually)
            procdb_file = files('procdbtools').joinpath('experiment_info5.db')


        engine = create_engine("sqlite:///{}".format(procdb_file))
        Session = sessionmaker(bind=engine)
        self.session = Session()



    def find_experiments(self, starttime, endtime):
        """
        Return list of all experiments between two times
        """

        # Get instrument ID number
        # Consider moving this outside of function?  Should be constant for class
        radar_shortname = self.radar.replace('-','').lower()
        site = self.session.query(Site).filter(Site.shortname==radar_shortname).one()
        inst_id = site.id

        # Find experiment by start/end times and radar id
        ustarttime = (starttime-dt.datetime.utcfromtimestamp(0)).total_seconds()
        uendtime = (endtime-dt.datetime.utcfromtimestamp(0)).total_seconds()
        conditions = sqlalchemy.and_(Experiment.site_id==inst_id, Experiment.end_time>ustarttime, Experiment.start_time<uendtime)
        filt_exp = self.session.query(Experiment).filter(conditions).all()

        return filt_exp

    def experiment_number(self, starttime, endtime):
        """
        Return just a list of experiment numbers
        """
        exp_list = self.find_experiments(starttime, endtime)
        exp_num = [exp.experiment for exp in exp_list]
        return exp_num

    def get_mode(self, exp):
        mode_id = exp.mode_id
        mode = self.session.query(RadarMode).filter(RadarMode.id==mode_id).one()
        return mode.name


    def experiment_path(self, exp, procdir='/Volumes/AMISR_PROCESSED/processed_data'):
        """
        Return the full path to a given experiment directory
        """

        mode = self.get_mode(exp)

        expdir = pathlib.Path(procdir, self.radar, f'{exp.start_year:04}', f'{exp.start_month:02}', mode, exp.experiment)

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




    def site_coords(self):
        radar_shortname = self.radar.replace('-','').lower()
        site = self.session.query(db.Site).filter(db.Site.shortname==radar_shortname).one()
        return site
    
    
