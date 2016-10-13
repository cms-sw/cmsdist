### RPM external py2-h5py 2.6.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/%{my_name}/%{my_name}/archive/%{realversion}.tar.gz
Requires: python py2-numpy hdf5 py2-six
BuildRequires: py2-setuptools cython py2-pkgconfig

%prep
%setup -n %{my_name}-%{realversion}

%build
export HDF5_DIR=${HDF5_ROOT}
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -print0 | xargs -0 rm -rf
