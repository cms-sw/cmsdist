### RPM external py3-imagesize 0.7.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/53/72/6c6f1e787d9cab2cc733cf042f125abec07209a58308831c9f292504e826/imagesize-0.7.1.tar.gz
Requires: python3 py3-certifi py3-urllib3 py3-idna py3-chardet
BuildRequires: py3-setuptools

%prep
%setup -n imagesize-%realversion

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
