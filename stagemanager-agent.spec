### RPM cms stagemanager-agent 0.0.2
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define wmcver WMCORE_0_7_2
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_stagemanager.tar.gz
Source1: %svnserver/StageManager/trunk/src/python@12925?scheme=svn+ssh&strategy=export&module=StageManager&output=/src.tar.gz

Requires: python
# py2-simplejson py2-sqlalchemy py2-httplib2 rotatelogs

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n StageManager

%build
cd ../WMCore
python setup.py build_system -s wmc-database
#cd ../StageManager
#python setup.py build

%install
cd ../WMCore
python setup.py install_system -s wmc-database --prefix=%i
#cd ../StageManager
#python setup.py install --prefix=%i
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/
cp -r ../StageManager %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/
find %i -name '*.egg-info' -exec rm {} \;

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
