# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:01:23 2018

@author: root
"""

import qcodes as qc
import numpy as np
from qdev_wrappers.station_configurator import StationConfigurator
from qdev_wrappers.logger import start_logging
from qdev_wrappers.sweep_functions import do1d, do2d
from qdev_wrappers.file_setup import all_init
import warnings

start_logging()

#scfg = StationConfigurator()
scfg = StationConfigurator('station_conf.yml')
all_init(sample_name='testtest', station=scfg.station, datafolder='data', subfolders=['analyses', 'pptxdumps'])

#mock_dac = scfg.load_instrument('qdac')
#mock_dmm = scfg.load_instrument('dmm1')
