import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from qcd3pt import *
from helpers import *


# data importing
rawFilename = 'data/p2gg_local_neutral_light.p-lvc-lvc.fl1.qx0_qy0_qz0.gseq_4.tseq_15.px0_py-2_pz2.h5'
arrFilename = 'data/confs.npy'
#test
load_mean_data(rawFilename, arrFilename, True)
