### RPM cms asyncstageout test_tag2
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source0: svn://svn.cern.ch/reps/CMSDMWM/WMCore/tags/0.7.11?scheme=svn+ssh&strategy=export&module=WMCore&output=/src_wmc_asyncstageout.tar.gz
Source1: svn://svn.cern.ch/reps/CMSDMWM/AsyncStageout/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=AsyncStageout&output=/src_asyncstageout.tar.gz
Requires: py2-simplejson py2-sqlalchemy py2-httplib2 rotatelogs
Patch0: asyncstageout-setup

%prep
%setup -D -T -b 1 -n AsyncStageout
%setup -T -b 0 -n WMCore
%patch0 -p0

%build
python setup.py build_system -s asyncstageout

%install
python setup.py install_system -s asyncstageout --prefix=%i
cp -pr ../AsyncStageout/src/python/AsyncStageOut %i/$PYTHON_LIB_SITE_PACKAGES/
cp -pr ../AsyncStageout/src/couchapp %i/
cp -pr ../AsyncStageout/configuration %i/
find %i -name '*.egg-info' -exec rm {} \;

# Generate .pyc files.
python -m compileall %i/$PYTHON_LIB_SITE_PACKAGES/AsyncStageOut || true

mkdir -p %i/bin
cp -pf %_builddir/WMCore/bin/{wmcoreD,wmcore-db-init,wmcore-new-config} %i/bin/

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
