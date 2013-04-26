### RPM cms dbs-web V06_00_52
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=DBS/Web/DataDiscovery&nocache=true&export=DBS&tag=-r%{cvstag}&output=/dbs-web.tar.gz

Requires: python mysql py2-mysqldb py2-simplejson elementtree
Requires: webtools dbs-client rotatelogs

%prep
%setup -n DBS/Web/DataDiscovery

%build

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
cp -r * %i/$PYTHON_LIB_SITE_PACKAGES

# Compile cheetah templates.
cd %i/$PYTHON_LIB_SITE_PACKAGES
mkdir -p rss
./scripts/genTemplates.sh

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
