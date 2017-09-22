### RPM external py3-cherrypy 5.4.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://github.com/cherrypy/cherrypy/archive/v%realversion.tar.gz
Requires: python3
Patch0: cherrypy-multipart-length

%prep
%setup -n cherrypy-%realversion
%patch0 -p0
perl -p -i -e 's/import profile/import cProfile as profile/' cherrypy/lib/profiler.py

%build
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
