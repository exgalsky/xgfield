import lpt
from xgfield import fieldsky
import sys
import numpy as np
import os

N      = 768
Lbox   = 7700.
Nside  = 1024
input  = 'cube'

parallel = False
ID = sys.argv[1]
if sys.argv[2] == 'parallel':
    parallel = True

try:
    path2disp = os.environ['LPT_DISPLACEMENTS_PATH']
except:
    path2disp = '/Users/shamik/Documents/Work/websky_datacube/'

cube = lpt.Cube(N=N,partype=None)

convert=np.array
starty=0
stopy=N
if parallel:
    import jax
    import jax.numpy as jnp
    convert=jnp.array

    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank  = comm.Get_rank()
    nproc = comm.Get_size()
    starty = N//nproc*rank
    stopy  = N//nproc*(rank+1)

cube.s1x = convert(np.reshape(np.fromfile(path2disp+'sx1_7700Mpc_n6144_nb30_nt16_no768',dtype=np.float32),(N,N,N)))[:,starty:stopy,:]
cube.s1y = convert(np.reshape(np.fromfile(path2disp+'sy1_7700Mpc_n6144_nb30_nt16_no768',dtype=np.float32),(N,N,N)))[:,starty:stopy,:]
cube.s1z = convert(np.reshape(np.fromfile(path2disp+'sz1_7700Mpc_n6144_nb30_nt16_no768',dtype=np.float32),(N,N,N)))[:,starty:stopy,:]

cube.s2x = convert(np.reshape(np.fromfile(path2disp+'sx2_7700Mpc_n6144_nb30_nt16_no768',dtype=np.float32),(N,N,N)))[:,starty:stopy,:]
cube.s2y = convert(np.reshape(np.fromfile(path2disp+'sy2_7700Mpc_n6144_nb30_nt16_no768',dtype=np.float32),(N,N,N)))[:,starty:stopy,:]
cube.s2z = convert(np.reshape(np.fromfile(path2disp+'sz2_7700Mpc_n6144_nb30_nt16_no768',dtype=np.float32),(N,N,N)))[:,starty:stopy,:]

sky = fieldsky.FieldSky(ID      = ID,
                        N       = N,
                        Lbox    = Lbox,
                        Nside   = Nside,
                        nlpt    = 2,
                        input   = input,
                        gpu     = parallel,
                        mpi     = parallel,
                        cube    = cube,
                        is64bit = False,
                        peak_per_cell_memory_in_MB = 75.)

sky.generate()
