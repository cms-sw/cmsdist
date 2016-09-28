### RPM external py2-h5py 2.6.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
%define my_name %(echo %n | cut -f2 -d-)
Source: https://github.com/%{my_name}/%{my_name}/archive/%{realversion}.tar.gz
Requires: python py2-numpy hdf5
BuildRequires: py2-setuptools hdf5

%prep
%setup -n %{my_name}-%{realversion}

%build
export CPLUS_INCLUDE_PATH=${HDF5_ROOT}/include
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -print0 | xargs -0 rm -rf
