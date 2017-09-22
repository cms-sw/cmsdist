### RPM external py3-elementtree 1.2.6
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://effbot.org/downloads/elementtree-%realversion-20050316.zip
Requires: python3
 
%prep
%setup -n elementtree-%realversion-20050316

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency
