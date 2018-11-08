### RPM external py2-h5py 2.8.0
## IMPORT build-with-pip

Requires: py2-numpy hdf5 py2-six
BuildRequires: py2-cython py2-pkgconfig
%define PipPreBuild export HDF5_DIR=${HDF5_ROOT}
