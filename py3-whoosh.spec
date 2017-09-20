### RPM external py3-whoosh 2.7.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/W/Whoosh/Whoosh-%{realversion}.tar.gz

Requires: python3
BuildRequires: py3-sphinx py3-setuptools

%prep
%setup -n Whoosh-%{realversion}

%build
python3 setup.py build

%install
python3 setup.py install -O1 --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
