### RPM external py2-h5py 2.7.1
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Requires: python py2-numpy hdf5 py2-six
BuildRequires: py2-setuptools py2-cython py2-pkgconfig



%define pip_name h5py

%define PipPreBuild export HDF5_DIR=${HDF5_ROOT}

## IMPORT build-with-pip

#%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
