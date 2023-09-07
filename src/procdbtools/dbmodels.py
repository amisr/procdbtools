import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint

Base = declarative_base()

class Experiment(Base):
    __tablename__ = 'experiment'

    id = Column(Integer, primary_key = True)
    experiment   = Column(String(12), nullable=False)   # typically, yyyymmdd.xxx
    nas_id = Column(Integer, ForeignKey('nas.id'), 
                    nullable=False)# folder as mounted on Appleton
    mode_id      = Column(Integer, ForeignKey('radarmode.id'),
                    nullable=False)  # mode the radar was running e.g. WorldDay40.v01
    site_id     = Column(Integer, ForeignKey('site.id'),nullable=False)
    start_year  = Column(Integer, nullable=False)
    end_year    = Column(Integer, nullable=False)
    start_month = Column(Integer, nullable=False)
    end_month   = Column(Integer, nullable=False)
    start_day   = Column(Integer, nullable=False)
    end_day     = Column(Integer, nullable=False)
    start_time  = Column(Integer, nullable=False)  # unix time
    end_time    = Column(Integer, nullable=False)  # unix time
    total_seconds    = Column(Integer, nullable=False) # total time experiment ran for
    start_filenumber = Column(Integer, nullable=False)  # filenumbers as output by radac e.g. d00011234
    end_filenumber   = Column(Integer, nullable=False)  # filenumbers as output by radac e.g. d00011234
    filesize = Column(Float, nullable=False) # total size in MB of experiments
    aeurx = Column(Float, nullable=True) # median aeurx in the experiment
    aeutx = Column(Float, nullable=True) # median aeutx in the experiment
    txpower = Column(Float, nullable=True) # median txpower in the experiment

    __table_args__ = (UniqueConstraint('experiment', 'nas_id',
        name='_experiment_directory_uc'),)

class Nas(Base):
    __tablename__ = 'nas'

    id = Column(Integer, primary_key=True)
    directory = Column(String(1024), nullable=False)

class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)
    shortname = Column(String(5), nullable=False)
    name = Column(String(128), nullable=False)
    code = Column(Integer, nullable=False)
    altitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class RadarMode(Base):
    __tablename__ = 'radarmode'

    id = Column(Integer, primary_key=True)
    site_id     = Column(Integer, ForeignKey('site.id'),nullable=False)
    name = Column(String(64), nullable=False, unique=True) # something like WorldDay40.v01
    name_inside_expfile = Column(String(64), nullable=True)
    #beams = Column(String(2048), nullable=False) # comma separated sorted string of beam codes e.g. '64047,64517'
    num_beams = Column(Integer, nullable=False)
    num_dtcs  = Column(Integer, nullable=False)
    modes     = Column(String(64), nullable=True) # from *.exp [Modes]
    
    #dtc0_id = Column(Integer, ForeignKey('dtcconfig.id'), nullable=True)
    #dtc1_id = Column(Integer, ForeignKey('dtcconfig.id'), nullable=True)
    #dtc2_id = Column(Integer, ForeignKey('dtcconfig.id'), nullable=True)
    #dtc3_id = Column(Integer, ForeignKey('dtcconfig.id'), nullable=True)


class DTCConfig(Base):
    # name format is "radarmode.name_dtc#"" e.g. WorldDay40.v01_dtc0
    __tablename__ = 'dtcconfig'

    id = Column(Integer, primary_key=True)
    radarmode_id = Column(Integer, ForeignKey('radarmode.id'), nullable=True)
    dtc = Column(Integer, nullable=False) # either 0,1,2,...
    #name = Column(String(128), nullable=False) # e.g. WorldDay40.v01_dtc0
    host_name  = Column(String(32), nullable=True)   # from *.exp [Hosts] |- DTC0=13 baud Barker code
    codetype   = Column(String(32), nullable=False)  # either coherent, incoherent, uncoded
    # pulsename  = Column(String(128), nullable=False)  # either barker, m-code, alternating code, long pulse
    # code = Column(String(128), nullable=False)  # string of the hex of the code
    processing = Column(String(32), nullable=False)  # CohCode, IncohCodeFl, S, PLFFTS, etc.
    tx_frequency  = Column(Integer, nullable=False)
    rx_frequency  = Column(Integer, nullable=False)
    has_raw       = Column(Boolean, nullable=False)
    # has_cal       = Column(Boolean, nullable=False)
    # has_noise     = Column(Boolean, nullable=False)
    # baud_length   = Column(Integer, nullable=False) # length of each baud in microseconds
    # pulse_length  = Column(Integer, nullable=False) # length of the pulse in microseconds
    sample_length = Column(Integer, nullable=False) # length of the voltage sample in microseconds

    __table_args__ = (UniqueConstraint('radarmode_id', 'dtc',
        name='_radarmode_dtc_uc'),)

class ModeBeam(Base):
    __tablename__ = 'modebeam'

    radarmode_id = Column(Integer, ForeignKey('radarmode.id'), primary_key=True)
    beam_id = Column(Integer, ForeignKey('beaminfo.id'), primary_key=True)

class BeamInfo(Base):
    __tablename__ = 'beaminfo'
    
    id = Column(Integer, primary_key=True)
    site_id     = Column(Integer, ForeignKey('site.id'),nullable=False)
    beamcode = Column(String(5), nullable=False)
    azimuth = Column(Float, nullable=True)
    elevation = Column(Float, nullable=True)
    system_constant = Column(Float, nullable=True)
    
    __table_args__ = (UniqueConstraint('beamcode', 'azimuth', 'elevation', 'system_constant',
        name='_bm_az_el_ksys_uc'),)

