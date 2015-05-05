### RPM external py2-pyfits 3.1.2
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define download_name %(echo "%{n}" | sed 's/py2-//')

Source: http://pypi.python.org/packages/source/p/%{download_name}/%{download_name}-%{realversion}.tar.gz
Requires: python 
BuildRequires: py2-numpy


%prep
%setup -q -n %{download_name}-%{realversion}

%build
#sed -i'' "s:\(library_dirs =\)\(.*\):\1 ${PYTHON_ROOT}\/lib:g" setup.cfg
#sed -i'' "s:\(include_dirs =\)\(.*\):\1 ${PYTHON_ROOT}\/include:g" setup.cfg
#sed -i'' "s:\(defines = \)\(.*\):\1 HAVE_TLS HAVE_LIBLDAP_R:g" setup.cfg

python setup.py build

%install

#mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
#export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}

rm -rf %{i}/${PYTHON_LIB_SITE_PACKAGES}/*.egg-info
