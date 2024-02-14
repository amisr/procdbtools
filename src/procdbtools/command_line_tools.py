# command_line_tools.py
# Command line utilities to quickly look up experiment and path for a given date and radar

import argparse
import datetime as dt
from procdbtools.amisr_lookup import AMISR_lookup

def lookup_single_time(radar, time):
    al = AMISR_lookup(radar)
    exp = al.find_experiment(time)
    if exp:
        mode = al.get_mode(exp)
        # print report
        print('{:20}{:25}'.format('Exp Num', exp.name))
        print('{:20}{:25}'.format('Concat Exp Num', exp.master_exp))
        print('{:20}{:25}'.format('Mode', mode))
        print('{:20}{:25}'.format('Start Time', str(exp.start_time)))
        print('{:20}{:25}'.format('End Time', str(exp.end_time)))
    else:
        print('No Experiment at this time.')

def lookup_time_range(radar, starttime, endtime):
    al = AMISR_lookup(radar)
    exp_list = al.find_experiments(starttime, endtime)
    # print report    
    print('{:14}{:20}{:14}'.format('Exp Num', 'Mode', 'Concat Exp Num'))
    for exp in exp_list:
        mode = al.get_mode(exp)
        print('{:14}{:20}{:14}'.format(exp.name, mode, exp.master_exp))


def main():
    parser = argparse.ArgumentParser(
                        prog='amisrdbquery',
                        description='Basic utility to quickly look up the AMISR experiment number and mode for a given datetime.')
    
    parser.add_argument('radar')
    parser.add_argument('time', default=None)
    parser.add_argument('-et', '--endtime')
    
    args = parser.parse_args()
    time = dt.datetime.fromisoformat(args.time)
    
    if args.endtime:
        endtime = dt.datetime.fromisoformat(args.endtime)
        lookup_time_range(args.radar, time, endtime)
    else:
        lookup_single_time(args.radar, time)

if __name__=='__main__':
    main()
