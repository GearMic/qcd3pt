import numpy as np
import matplotlib.pyplot as plt

from qcd3pt import *
from helpers import *

def plot_confs(confs, filenames):
    data = np.mean(confs, 0)
    #data = confs[0]
    # TODO: calculate covariance matrices
    dataErr = np.std(confs, 0, ddof=1) / np.sqrt(confs.shape[0])
    #dataCov = np.cov(confs.T, ddof=1) / confs.shape[0]
    time = np.arange(data.shape[-1])

    ndim = 4
    for mu in range(ndim):
        fig, ax = plt.subplots()
        for nu in range(ndim):
            dataPlot = data[mu, nu, :].real
            dataPlotErr = dataErr[mu, nu, :].real

            #ax.plot(time, dataPlot, 'x', label='$\\nu=%i$'%nu)
            ax.errorbar(time, dataPlot, dataPlotErr, fmt='x', label='$\\nu=%i$'%nu)

        ax.set_xlabel(r'$t$')
        ax.set_ylabel(r'$C_{\mu\nu}^{(3)}(t)$')
        ax.set_title('$\\mu=%i$' % mu)
        ax.legend()
        fig.savefig(filenames[mu])
    #ax.set_ylim(-0.0005, 0.0015)

# data importing
rawFilename = 'data/p2gg_local_neutral_light.p-lvc-lvc.fl1.qx0_qy0_qz0.gseq_4.tseq_15.px0_py-2_pz2.h5'
arrFilename = 'data/confs.npy'
#test
confs = load_mean_data(rawFilename, arrFilename, True)
print(confs.shape)
plot_confs(confs, ('plot/confs_mu0.pdf', 'plot/confs_mu1.pdf', 'plot/confs_mu2.pdf', 'plot/confs_mu3.pdf'))
