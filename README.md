# procdbtools
Toolkits for finding experiments and files in the processed AMISR database.

Although anyone is welcome to use this code, it is likely primarily useful internally at SRI.

## Install
This package can be installed with pip.  It is not currently hosted on pypi, so you must either clone the repository or install directly from GitHub.

**Clone Repository:**

```
$ git clone https://github.com/amisr/procdbtools.git
$ cd procdbtools
$ pip install .
```

**Install from GitHub:**

```
pip install git+https://github.com/amisr/procdbtools.git
```

The package requires [sqlalchemy](https://www.sqlalchemy.org/), which should be installed automatically with pip.

Before using the package for the first time, you will have to obtain the database SQL file.  Follow the instructions in the "Update SQL Database" section below to to this.


## Usage
This package provides a command line tool and a module to be used in python scripts.

### Command Line
The `amisrdbquery` command line utility will list what processed experiments are available during a given time.  Use the name of the radar and time (ISO format) as command line arguments.

To display details about the experiment that was running at a particular time:
```
$ amisrdbquery RADAR YYYY-MM-DDTHH:MM:SS
```

To list all experiments run between two times, use the `-st` (start time) and `-et` (end time) flags:
```
$ amisrdbquery RADAR -st YYYY-MM-DDTHH:MM:SS -et YYYY-MM-DDTHH:MM:SA
```

To list all experiments run on a given day:
```
$ amisrdbquery RADAR YYYY-MM-DD
```

### Python
The `AMISR_lookup` class can be imported and initialized with the name of the radar.

```
from procdbtools.amisr_lookup import AMISR_lookup
amisrdb = AMISR_lookup('PFISR')
```

Methods of this class can then be used to determine what experiments are avaiable over different periods of time.

```
import datetime as dt
time0 = dt.datetime(2024, 5, 11, 12, 0, 0, 0)

# Find the experiment at this time
exp = amisrdb.find_experiment(time0)

# Find the mode for this experiment
mode = amisrdb.get_mode(exp)

# Find the experiment number
exp_num = amisrdb.get_experiment_number(exp)

# Find the standard path to this experiment
path = amisrdb.experiment_path(exp)

# Find the actual filename
filename = amisrdb.select_datafile(exp, pulse='lp')
```

Note that the experiment path and datafile functionality will only be available if run on a system with access to the processed AMISR database.  By default, this is assumed to exist at `/Volumes/AMISR_PROCESSED/processed_data`, but this can be changed with the optional `db_path` parameter when initalizing the `AMISR_lookup` class.

The `select_datafile` method has three options, `pulse`, `integration`, and `cal`.  The `pulse` option MUST be specified to indicate the pulse coding to select.  If `integration` is not specified, the minimum integration time available down to `1min` will be chosen.  If `cal` is not specified, a processed file is selected following the priorty `fitcal`, `cal`, and nothing.

## Update SQL Database
The package uses a local copy of the processed AMISR SQL database.  As time passes and you query more recent files, this will need to be updated manually.  The reference version of the SQL database is generated daily on io2.

First, copy the latest version of the database:
```
$ scp io2:/opt/websites/database/calendar/isr_database/amisrdb .
```

Then, run the following python code to update the local copy that `procdbtools` uses:
```
> from procdbtools.manage_database import update_db_file
> update_db_file('amisrdb')
```

