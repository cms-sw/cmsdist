### RPM cms T0DataSvc 5.0.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define wmcver WMCORE_0_7_2
%define moduleName T0
%define exportName T0
%define cvstag T0DataSvc-5_0_1
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_t0datasvc.tar.gz
Source1: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah yui
Requires: rotatelogs py2-cx-oracle

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n %{moduleName}

%build
cd ../WMCore
python setup.py build_system -s wmc-web

%install
cd ../WMCore
python setup.py install_system -s wmc-web --prefix=%i
tar -C src/python -cf - WMCore/HTTPFrontEnd/WorkQueue/Services/ServiceInterface.py |
 tar -C %i/lib/python*/site-packages -xvvf -
find %i/lib/python*/site-packages/WMCore/HTTPFrontEnd -type d -exec touch {}/__init__.py \;

cd ../%{moduleName}
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/
cp -r src/python/T0 %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/
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
