import numpy as np 
import xgcosmo.cosmology as cosmo 
import healpy as hp 
import liblightcone as llc
import xgutil.backend as bk
import os
import argparse
import fieldmock.defaults as fmdefaults

import logging
log = logging.getLogger("LIGHTCONE")

class FieldSky:
    '''FieldSky'''
    def __init__(self, **kwargs):

        self.ID    = kwargs.get(   'ID',fmdefaults.ID)
        self.N     = kwargs.get(    'N',fmdefaults.N)
        self.Lbox  = kwargs.get( 'Lbox',fmdefaults.Lbox)
        self.Nside = kwargs.get('Nside',fmdefaults.Nside)
        self.ityp  = kwargs.get( 'ityp',fmdefaults.ityp)

    def generate(self, **kwargs):

        times={'t0' : time()}

        grid_nside = self.N # cube shape is parameterized by grid_nside; full resolution for websky is 6144
        map_nside  = self.Nside
        L_box      = self.Lbox

        # ------ hardcoded parameters
        comov_lastscatter_Gpc = 13.8  # conformal distance to last scattering surface in Gpc
        zmin                  = 0.05  # minimum redshift for projection (=0.05 for websky products)
        zmax                  = 4.5   # maximum redshift for projection (=4.50 for websky products)

        force_no_mpi          = False 
        force_no_gpu          = False

        kappa_map_filebase = f'./output/kappa_1lpt_grid-{ grid_nside }_nside-{ map_nside }'

        backend = bk.backend(force_no_mpi=force_no_mpi, force_no_gpu=force_no_gpu)
        backend.print2log(log, f"Backend configuration complete.", level='usky_info')

        # Paths to displacement fields
        try:
            path2disp = os.environ['LPT_DISPLACEMENTS_PATH']
        except:
            path2disp = '/Users/shamik/Documents/Work/websky_datacube/'

        backend.print2log(log, f"Path to displacement files set to {path2disp}", level='usky_info')

        if grid_nside == 768:
            sxfile = path2disp+'sx1_7700Mpc_n6144_nb30_nt16_no768'
            syfile = path2disp+'sy1_7700Mpc_n6144_nb30_nt16_no768'
            szfile = path2disp+'sz1_7700Mpc_n6144_nb30_nt16_no768'
        else:
            sxfile = path2disp+'sx1_7700Mpc_n6144_nb30_nt16'
            syfile = path2disp+'sy1_7700Mpc_n6144_nb30_nt16'
            szfile = path2disp+'sz1_7700Mpc_n6144_nb30_nt16'

        backend.print2log(log, f"Computing cosmology...", level='usky_info')
        cosmo_wsp = cosmo.cosmology(backend, Omega_m=0.31, h=0.68) # for background expansion consistent with websky
        backend.print2log(log, f"Cosmology computed", level='usky_info')

        backend.print2log(log, f"Setting up lightcone workspace...", level='usky_info')
        lpt_wsp = llc.lightcone_workspace(cosmo_wsp, grid_nside, map_nside, L_box, zmin, zmax)

        backend.print2log(log, f"Computing LPT to kappa map...", level='usky_info')
        kappa_map = lpt_wsp.lpt2map([sxfile, syfile, szfile], backend, bytes_per_cell=4)
        backend.print2log(log, f"Kappa map computed. Saving to file.", level='usky_info')

        backend.mpi_backend.writemap2file(kappa_map, kappa_map_filebase+".fits")
        backend.print2log(log, f"LIGHTCONE: Kappa map saved. Exiting...", level='usky_info')




