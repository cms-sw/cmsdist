### RPM external py3-pyrex 0.9.9
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/Pyrex-%realversion.tar.gz
Requires: python3

%prep
%setup -n Pyrex-%realversion

%build
sed -i -e "s,execfile(distutils.util.convert_path('Pyrex/Compiler/Version.py')),exec(open(distutils.util.convert_path('Pyrex/Compiler/Version.py')).read()),g" setup.py
python3 setup.py build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
