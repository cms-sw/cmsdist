### RPM external py3-jsonpath-rw 1.2.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/j/jsonpath-rw/jsonpath-rw-%{realversion}.tar.gz
Requires: python3 py3-six
BuildRequires: py3-setuptools

%prep
%setup -n jsonpath-rw-%{realversion}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null

find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
