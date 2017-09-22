### RPM external py3-requests 2.18.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/b0/e1/eab4fc3752e3d240468a8c0b284607899d2fbfb236a56b7377a329aa8d09/requests-2.18.4.tar.gz
Requires: python3 py3-certifi py3-urllib3 py3-idna py3-chardet
BuildRequires: py3-setuptools

%prep
%setup -n requests-%realversion

%build
export PYTHON3_ROOT
python3 setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
export LD_LIBRARY_PATH=$PYTHON3_ROOT/lib:$LD_LIBRARY_PATH
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
