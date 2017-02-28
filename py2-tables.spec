### RPM external py2-tables 3.3.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
Patch0: py2-tables-fix-for-aarch64
%define pip_name tables
Requires: py2-numexpr py2-six py2-numpy hdf5 bz2lib

%define PipPreBuild export HDF5_DIR=${HDF5_ROOT} && tar -xzf tables-%{realversion}.tar.gz && pushd tables-%{realversion} && for pch in %{patches} ; do patch -p1 < ${pch} ; done && popd && rm -f tables-%{realversion}.tar.gz && tar czf tables-%{realversion}.tar.gz  tables-%{realversion}

%define PipBuildOptions  --global-option="--hdf5=${HDF5_ROOT}" --global-option="--bzip2=${BZ2LIB_ROOT}" 

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/pttree %{i}/bin/pt2to3 %{i}/bin/ptrepack %{i}/bin/ptdump

