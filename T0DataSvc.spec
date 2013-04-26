### RPM cms T0DataSvc 5.0.5
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define wmcver 0.8.3
%define moduleName T0
%define exportName T0
%define cvstag T0DataSvc-5_0_5
%define cvsserver cvs://:pserver:anonymous@cmssw.cvs.cern.ch:/local/reps/CMSSW?passwd=AA_:yZZ3e
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_t0datasvc.tar.gz
Source1: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah yui
Requires: rotatelogs py2-cx-oracle

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n %{moduleName}
perl -p -i -e '/from WMCore.HTTPFrontEnd.WorkQueue.Services.ServiceInterface import ServiceInterface/
               && s/WMCore.HTTPFrontEnd.WorkQueue/T0.DAS/' src/python/T0/DAS/Services/*.py

%build
cd ../WMCore
python setup.py build_system -s wmc-web

%install
cd ../WMCore
python setup.py install_system -s wmc-web --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

cd ../%{moduleName}
tar -C src/python -cf - T0/DAS | tar -C %i/lib/python*/site-packages -xvvf -
find %i/lib/python*/site-packages/T0 -type d -exec touch {}/__init__.py \;

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES || true

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
