### RPM external py3-sphinxcontrib-websupport 1.0.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/c5/6b/f0630436b931ad4f8331a9399ca18a7d447f0fcc0c7178fb56b1aee68d01/sphinxcontrib-websupport-1.0.1.tar.gz
Requires: python3 py3-sphinx
BuildRequires: py3-setuptools

%prep
%setup -n sphinxcontrib-websupport-%realversion

%build
export PY3_SPHINX_ROOT
pver=`python3 -V | awk '{print $2}' | cut -d . -f 1,2`
export PYTHONPATH=$PY3_SPHINX_ROOT/lib/python$pver/site-packages:$PYTHONPATH
python3 setup.py build

%install
export PY3_SPHINX_ROOT
pver=`python3 -V | awk '{print $2}' | cut -d . -f 1,2`
export PYTHONPATH=$PY3_SPHINX_ROOT/lib/python$pver/site-packages:$PYTHONPATH
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
