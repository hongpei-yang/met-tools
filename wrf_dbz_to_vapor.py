### This is a python code used to create a netcdf file containing
### radar reflectivity (REF) that extracted from wrf output.
### This netcdf file then could be used for REF visualization using VAPOR
### ©Hongpei Yang 2025, Sun Yat-sen University


### import packages
import numpy as np
from netCDF4 import Dataset
import wrf

### read wrf output file
# Open the NetCDF file
ncfile1 = Dataset('/Volumes/T7-yanghp/proj_ongoing/downhill_CI/WRF_data/wrfout_d02_2024-08-04_0000_ctrl')
# Get the WRF variables
z = wrf.getvar(ncfile1,"z",0)
it = 22 # set the time 
dbz = wrf.getvar(ncfile1,"dbz",it) # composite radar
xlat = wrf.getvar(ncfile1,"XLAT",it)
xlon = wrf.getvar(ncfile1,"XLONG",it)
topo = wrf.getvar(ncfile1,"ter",it)
znu  = wrf.getvar(ncfile1,"ZNU",it)

dbz_3d = np.array(dbz)   # (nz, ny, nx)
topo2d = np.array(topo) # (ny, nx)
lat2d  = np.array(xlat)  # (ny, nx)
lon2d  = np.array(xlon)  # (ny, nx)
znu1d  = np.array(znu)   # nz

nz, ny, nx = dbz_3d.shape

### Create and open NetCDF file
out_nc = Dataset('topo_dbz3d_vapor_ready.nc', 'w', format='NETCDF4')

out_nc.createDimension('z', nz)
out_nc.createDimension('y', ny)
out_nc.createDimension('x', nx)

z_var = out_nc.createVariable('z', 'f4', ('z',))
y_var = out_nc.createVariable('y', 'f4', ('y',))
x_var = out_nc.createVariable('x', 'f4', ('x',))

z_var[:] = znu1d.astype('f4')     # physical layers
y_var[:] = lat2d[:,0].astype('f4')   
x_var[:] = lon2d[0,:].astype('f4')   

z_var.units = 'm'
y_var.units = 'degrees_north'
x_var.units = 'degrees_east'
z_var.positive = 'up'

### write variables
dbz_var = out_nc.createVariable('DBZ', 'f4', ('z','y','x'), fill_value=np.nan)
dbz_var[:] = dbz_3d.astype('f4')
dbz_var.units = 'dBZ'
dbz_var.long_name = 'Radar reflectivity'
dbz_var.valid_range = np.array([-10.0, 70.0], dtype='f4')

topo_var = out_nc.createVariable('TOPO', 'f4', ('y','x'))
topo_var[:] = topo2d.astype('f4')
topo_var.units = 'm'

lat_var = out_nc.createVariable('XLAT', 'f4', ('y','x'))
lon_var = out_nc.createVariable('XLONG','f4', ('y','x'))
lat_var[:] = lat2d.astype('f4')
lon_var[:] = lon2d.astype('f4')
lat_var.units = 'degrees_north'
lon_var.units = 'degrees_east'

### Close NetCDF file
out_nc.close()
print("NetCDF file written: topo_dbz3d_vapor_ready.nc")
