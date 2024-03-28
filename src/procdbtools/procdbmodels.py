import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint

Base = declarative_base()

class ProcdbInstrument(Base):
    __tablename__ = 'procdb_instrument'

    id = Column(Integer, primary_key = True)
    abbr = Column(String(10), nullable=False)
    descriptor = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    code = Column(Integer, nullable=False)

class ProcdbExperiment(Base):
    __tablename__ = 'procdb_experiment'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    non_spinning_backup = Column(Boolean, nullable=False)
    start_time = Column(DateTime(), nullable=False)
    end_time = Column(DateTime(), nullable=False)
    note = Column(Text, nullable=False)
    proc_log = Column(Text, nullable=False)
    inst_id = Column(Integer, nullable=False)
    type_id = Column(Integer, nullable=False)
    cloud_backup = Column(Boolean, nullable=False)
    items = Column(String(30), nullable=False)
    master_exp = Column(String(50), nullable=False)
    status_date = Column(DateTime(), nullable=False)
    size = Column(String(10), nullable=False)

class ProcdbExperimentType(Base):
    __tablename__ = 'procdb_experimenttype'
    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)
    inst_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    abbr = Column(String(50), nullable=False)
 
