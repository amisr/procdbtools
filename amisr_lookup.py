# amisr_lookup.py
# Look up the experiment an AMISR radar was running in durring a particular period,
#   including mode/experiment information.
# Requires sqlalchemy and the appropriate AMISR SQL database

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
import pathlib
import re


class AMISR_lookup(object):

    def __init__(self, radar, procdb_file=None):

        self.radar = radar

        if not procdb_file:
            procdb_file = pathlib.Path(__file__).parent.resolve().joinpath('amisrdb')

        self.initialize_db(procdb_file)


    def initialize_db(self, procdb_file):
        Base = automap_base()
        engine = sqlalchemy.create_engine('sqlite:///'+str(procdb_file))
        Base.prepare(engine, reflect=True)
        self.session = sqlalchemy.orm.Session(engine)
        self.db = Base.classes

    def find_experiments(self, starttime, endtime):

        # Get instrument ID number
        # Consider moving this outside of function?  Should be constant for class
        inst_id = self.session.query(self.db.procdb_instrument).filter(self.db.procdb_instrument.abbr == self.radar).one().id

        # Find experiment by start/end times and radar id
        conditions = sqlalchemy.and_(self.db.procdb_experiment.inst_id==inst_id, self.db.procdb_experiment.end_time>starttime, self.db.procdb_experiment.start_time<endtime)
        filt_exp = self.session.query(self.db.procdb_experiment).filter(conditions)

        # Create list of experiments
        exp_list = list()
        for q in filt_exp:
            mode = self.session.query(self.db.procdb_experimenttype).filter(self.db.procdb_experimenttype.id == q.type_id).one().label
            exp_list.append({'exp_num':q.name, 'mode':mode, 'mast_exp':q.master_exp})

        return exp_list


    def experiment_path(self, exp, procdir='/Volumes/AMISR_PROCESSED/processed_data'):

        if exp['mast_exp']:
            experiment_number = exp['mast_exp']
        else:
            experiment_number = exp['exp_num']

        expdir = pathlib.Path(procdir, self.radar, experiment_number[0:4], experiment_number[4:6], exp['mode'], experiment_number)
        # print(expdir)

        # check if path exists before returning
        if not expdir.exists():
            expdir = expdir.with_name(experiment_number+'.done')

        if expdir.exists():
            return expdir
        else:
            return None

        # try:
        #     path = '/Volumes/AMISR_PROCESSED/processed_data/RISR-N/{}/{}/{}/{}'.format(exp.experiment[0:4],exp.experiment[4:6],exp.mode,exp.experiment)
        #     datafiles = [f for f in os.listdir(path) if (f.endswith('h5') and '_lp_' in f)]
        # except OSError:
        #     try:
        #         path = '/Volumes/AMISR_PROCESSED/processed_data/RISR-N/{}/{}/{}/{}.done'.format(exp.experiment[0:4],exp.experiment[4:6],exp.mode,exp.experiment)
        #         datafiles = [f for f in os.listdir(path) if (f.endswith('h5') and '_lp_' in f)]
        #     except OSError:
        #         continue



    def select_experiment_file(self, experiment_path, type='lp', check_exists=False):

        if not experiment_path:
            return None

        exp_num = experiment_path.name
        datafiles = [f.name for f in experiment_path.glob('*.h5')]
        # print(datafiles)



        # create list of "normal" fitted files, fitcal if available, then cal, then all others
        calfiles = [f for f in datafiles if re.match(r'{}_{}_\d+min-fitcal.h5'.format(exp_num, type), f)]
        if not calfiles:
            calfiles = [f for f in datafiles if re.match(r'{}_{}_\d+min-cal.h5'.format(exp_num, type), f)]
        if not calfiles:
            calfiles = [f for f in datafiles if re.match(r'{}_{}_\d+min.h5'.format(exp_num, type), f)]
        if not calfiles:
            return None


        # Get file with minimum time resolution
        timeres = [int(re.search(r'\d+min', f).group()[:-3]) for f in calfiles]
        datafile = calfiles[timeres.index(min(timeres))]

        filename = experiment_path.joinpath(datafile)

        if check_exists:
            if not filename.is_file():
                return None

        return filename



        # # choose file with shortest time resolution
        # try:
        #     timeres = [int(re.search(r'\d+min', f).group()[:-3]) for f in calfiles]
        #     datafile = calfiles[timeres.index(inttime)]
        #     # fileres = inttime
        #     postint = False
        # except ValueError:
        #     try:
        #         datafile = calfiles[timeres.index(min(timeres))]
        #         # fileres = min(timeres)
        #         postint = True
        #     except ValueError:
        #         continue
        #
        # print(os.path.join(path,datafile))
        # num_files += 1



    # def site_coords(self):
    #     site = db.Table('site', db.MetaData(), autoload=True, autoload_with=self.engine)
    #     query = db.select([site.columns.latitude, site.columns.longitude]).where(site.columns.shortname==self.radar.lower())
    #     radar_site = self.conn.execute(query).fetchall()[0]
    #     return radar_site
    #
    #
    # def __del__(self):
    #     self.conn.close()
