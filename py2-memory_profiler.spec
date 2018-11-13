### RPM external py2-memory_profiler 0.52.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://files.pythonhosted.org/packages/23/11/50a969d32a14cdec2cfd57bee2e67fd6f83715a04361ba230dbce562b9cb/memory_profiler-%realversion.tar.gz
Requires: python py2-psutil
BuildRequires: py2-setuptools

%prep
%setup -n memory_profiler-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
find %i -name '.package-checksum' -exec rm {} \;
