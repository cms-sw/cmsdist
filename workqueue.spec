### RPM cms workqueue 0.0.18
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define cvstag %v

#Source: svn://svn.cern.ch/reps/CMSDMWM/WMCore/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=WMCore&output=/src.tar.gz
Source: svn://svn.cern.ch/reps/CMSDMWM/WMCore/trunk@13232?scheme=svn+ssh&strategy=export&module=WMCore&output=/src.tar.gz

Requires: python py2-httplib2 pystack rotatelogs couchdb dbs-client dls-client py2-cjson

%prep
%setup -n WMCore

%build
python setup.py build_system -s workqueue

%install
python setup.py install_system -s workqueue --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pf %_builddir/WMCore/bin/*workqueue* %i/bin

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done


%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
