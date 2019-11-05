### RPM external py3-pymongo 3.9.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

#Source: http://pypi.python.org/packages/source/p/pymongo/pymongo-%realversion.tar.gz
Source: https://pypi.python.org/packages/82/26/f45f95841de5164c48e2e03aff7f0702e22cef2336238d212d8f93e91ea8/pymongo-%realversion.tar.gz
Requires: python3 py3-elementtree
BuildRequires: py3-setuptools

%prep
%setup -n pymongo-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
