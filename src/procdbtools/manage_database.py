# manage_database.py

from pathlib import Path

# Define procdbtools default directory
home_dir = Path.home()
procdbtools_dir = home_dir.joinpath('.procdbtools')
procdb_file = procdbtools_dir.joinpath('amisrdb')

def update_db_file(filename):

    if not procdbtools_dir.is_dir():
        procdbtools_dir.mkdir()

    Path(filename).rename(procdb_file)


