#from qdev_wrappers import logging

import atexit
import qcodes as qc
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#from chickpea import Segment, Waveform, Element, Sequence

#from qdev_wrappers.file_setup import CURRENT_EXPERIMENT, my_init
from qdev_wrappers.station_configurator import StationConfigurator
from qdev_wrappers.show_num import show_num, show_meta
from qdev_wrappers.sweep_functions import do1d, do2d, do0d
#from qdev_wrappers.transmon import *
from qdev_wrappers.qdev_fitter import qdev_fitter

station = qc.Station()

from qdev_wrappers.logger import start_logging
from qdev_wrappers.file_setup import all_init
import warnings

start_logging()

#scfg = StationConfigurator()
scfg = StationConfigurator('station_conf.yaml')
all_init(sample_name='testtest3', station=scfg.station, datafolder='data', subfolders=['analyses', 'pptxdumps'])



################
Lockin_Middle = scfg.load_instrument('Lockin_Stanford_Research_Middle')
Lockin_Lower = scfg.load_instrument('Lockin_Stanford_Research_Lower')
SG1 = scfg.load_instrument('RohdeSchwarz_SGS100A')
qdac = scfg.load_instrument('qdac')
keysight1 = scfg.load_instrument('SG_Keysight_33500B')
UHFLI = scfg.load_instrument('UHFLI')
mercuryIPS = scfg.load_instrument('mercuryIPS')
fridge = scfg.load_instrument('fridge') 


     
####################

#switch = scfg.load_instrument('switch')
#awg = scfg.load_instrument('awg')

#awg5208 = scfg.load_instrument('awg5208')
#dmm1 = scfg.load_instrument('dmm1')
#dmm2 = scfg.load_instrument('dmm2')
#keith = scfg.load_instrument('keith')
#qubit = scfg.load_instrument('qubit')
#cavity = scfg.load_instrument('cavity')
#vna = scfg.load_instrument('vna')
#mercury = scfg.load_instrument('mercury')
#mag_sphere = scfg.load_instrument('mag_sphere',paramX=mercury.x_fld, paramY=keith.By, paramZ=mercury.z_fld)
dummy_time = qc.ManualParameter('dummy_time')
#alazar = scfg.load_instrument('alazar')
#alazar_ctrl = scfg.load_instrument('alazar_ctrl')
#sample_mag = scfg.load_instrument('sample_mag',parent=alazar_ctrl)
#sample_phase = scfg.load_instrument('sample_phase',parent=alazar_ctrl)
#sample_rec_mag = scfg.load_instrument('sample_rec_mag',parent=alazar_ctrl)
#sample_rec_phase = scfg.load_instrument('sample_rec_phase',parent=alazar_ctrl)
#avg_f1_mag = scfg.load_instrument('avg_f1_mag',parent=alazar_ctrl)
#avg_f1_phase = scfg.load_instrument('avg_f1_phase',parent=alazar_ctrl)
#avg_f2_mag = scfg.load_instrument('avg_f2_mag',parent=alazar_ctrl)
#avg_f2_phase = scfg.load_instrument('avg_f2_phase',parent=alazar_ctrl)
#avg_f3_mag = scfg.load_instrument('avg_f3_mag',parent=alazar_ctrl)
#avg_f3_phase = scfg.load_instrument('avg_f3_phase',parent=alazar_ctrl)
#avg_f4_mag = scfg.load_instrument('avg_f4_mag',parent=alazar_ctrl)
#avg_f4_phase = scfg.load_instrument('avg_f4_phase',parent=alazar_ctrl)
#rec_f1_mag = scfg.load_instrument('rec_f1_mag',parent=alazar_ctrl)
#rec_f1_phase = scfg.load_instrument('rec_f1_phase',parent=alazar_ctrl)
#rec_f2_mag = scfg.load_instrument('rec_f2_mag',parent=alazar_ctrl)
#rec_f2_phase = scfg.load_instrument('rec_f2_phase',parent=alazar_ctrl)
#rec_f3_mag = scfg.load_instrument('rec_f3_mag',parent=alazar_ctrl)
#rec_f3_phase = scfg.load_instrument('rec_f3_phase',parent=alazar_ctrl)
#rec_f4_mag = scfg.load_instrument('rec_f4_mag',parent=alazar_ctrl)
#rec_f4_phase = scfg.load_instrument('rec_f4_phase',parent=alazar_ctrl)
#alazar_ctrl.channels.extend([sample_mag, sample_phase, 
#                             sample_rec_mag, sample_rec_phase, 
#                             avg_f1_mag, avg_f1_phase, avg_f2_mag, avg_f2_phase,
#                             avg_f3_mag, avg_f3_phase, avg_f4_mag, avg_f4_phase,
#                             rec_f1_mag, rec_f1_phase, rec_f2_mag, rec_f2_phase,
#                             rec_f3_mag, rec_f3_phase, rec_f4_mag, rec_f4_phase])
#alazar.sync_settings_to_card()
#pulse_builder = scfg.load_instrument('pulse_builder',awg=awg5208,alazar=alazar,alazar_ctrl=alazar_ctrl,qubit=qubit,cavity=cavity)

#lockinAmplitudeDivider = 1e4
#lockinLabels = ["MainWire","g"]
#
#for i,v in enumerate([Lockin_Middle]):
#    
#    v.X.unit = "e$^2$/h"
#    v.X.scale = 1e8 * (v.amplitude.get()/lockinAmplitudeDivider) * 3.874e-5 
#    v.X.label = lockinLabels[i]

# define extra functions
#Qdevfit = qdev_fitter()

# IEc

def Q1Plungers_set(value):
    qdac.Q1iP(value)
    qdac.Q1gP(value)
Q1Plungers = qc.Parameter('Q1Plungers',label='Q1Plungers',unit='V',set_cmd=Q1Plungers_set)

def Q2Plungers_set(value):
    qdac.Q2iP(value)
    qdac.Q2gP(value)
Q2Plungers = qc.Parameter('Q2Plungers',label='Q2 Plungers',unit='V',set_cmd=Q2Plungers_set)

def Q4Plungers_set(value):
    qdac.Q4iP(value)
    qdac.Q4gP(value)
Q4Plungers = qc.Parameter('Q4Plungers',label='Q4 Plungers',unit='V',set_cmd=Q4Plungers_set)

def AllGates_set(value):
    qdac.Q1C(value)
    qdac.Q1iP(value)
    qdac.Q1gP(value)
    qdac.Q2C(value)
    qdac.Q2iP(value)
    qdac.Q2gP(value)
    qdac.Q3C(value)
    qdac.Q3iP(value)
    qdac.Q3gP(value)
    qdac.Q4C(value)
    qdac.Q4iP(value)
    qdac.Q4gP(value)
AllGates = qc.Parameter('AllGates',label='AllGates',unit='V',set_cmd=AllGates_set)

# Older

def Q1Plungers_set(value):
    qdac.Q1P1(value)
    qdac.Q1P2(value)
Q1Plungers = qc.Parameter('Q1Plungers',label='Q1 Plungers',unit='V',set_cmd=Q1Plungers_set)

#def Q2Plungers_set(value):
#    qdac.Q2P1(value)
#    qdac.Q2P2(value)
#    qdac.Q2P3(value)
#    qdac.Q2P4(value)
#Q2Plungers = qc.Parameter('Q2Plungers',label='Q2 Plungers',unit='V',set_cmd=Q2Plungers_set)

def Q2Cutters_set(value):
    qdac.Q2C1(value)
    qdac.Q2C2(value)
Q2Cutters = qc.Parameter('Q2Cutters',label='Q2 Cutters',unit='V',set_cmd=Q2Cutters_set)

def Q2All_set(value):
    qdac.Q2P1(value)
    qdac.Q2P2(value)
    qdac.Q2P3(value)
    qdac.Q2P4(value)
    qdac.Q2C1(value)
    qdac.Q2C2(value)
Q2All = qc.Parameter('Q2All',label='Q2 All gates',unit='V',set_cmd=Q2All_set)

def Q2Pl12_set(value):
    qdac.Q2P1(value)
    qdac.Q2P2(value)
Q2P12 = qc.Parameter('Q2P12',label='Q2 1, 2 Plungers',unit='V',set_cmd=Q2Pl12_set)


#%%

#Extra stuff for multiqubit readout:
cal_traces = []
for i in range(pulse_builder.number_read_freqs):
    vna.add_channel(channel_name='S21_{}'.format(i+1),vna_parameter='S21')

# Commenting away below 20180614 -OE
# Not a good idea, CavSet stopped working because cal_traces is empty
# I just don't want VNA stuff to be changed around during initialization ...
for i in range(pulse_builder.number_read_freqs):
    vna.channels[i].status(1)
    vna.channels[i].span(40e6)
    vna.channels[i].center(getattr(pulse_builder,'readout_freq_{}'.format(i+1))())
    vna.channels[i].bandwidth(1000)
    vna.channels[i].avg(5)
    vna.channels[i].power(-40)
    vna.channels[i].format('Linear Magnitude')
    cal_traces.append(vna.channels[i].trace)
#vna.display_grid(2,2)
vna.rf_power(1)
switch.all(2)
time.sleep(2)
vna.channels.autoscale()
vna.channels.status(0)

from scripts.Task_functions import Alazar_Cavset, CavPrep
from functools import partial

Alazar_Cavset_Task = qc.Task(partial(Alazar_Cavset,cal_traces,pulse_builder,switch,qubit,detuning=-1e6))
CavPrep_Task = qc.Task(partial(CavPrep,switch,qubit))

#%% Stuff added by OE

# Short-hand measurement handles
twotone = [CavPrep_Task, vna.S21_1.trace, Alazar_Cavset_Task, alazar_ctrl.channels[12:14].data]
vnat = [vna.S21_1.trace]

def glc():
    return get_latest_counter()










