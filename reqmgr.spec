### RPM cms reqmgr 0.8.11
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source: svn://svn.cern.ch/reps/CMSDMWM/WMCore/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=WMCore&output=/src_reqmgr.tar.gz
#Source: svn://svn.cern.ch/reps/CMSDMWM/WMCore/trunk/?scheme=svn+ssh&strategy=export&module=WMCore&output=/src_reqmgr.tar.gz
Requires: py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah py2-cx-oracle yui rotatelogs couchdb py2-cjson

%prep
%setup -n WMCore

%build
python setup.py build_system -s reqmgr

%install
python setup.py install_system -s reqmgr --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pf %_builddir/WMCore/bin/[[:lower:]]* %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
