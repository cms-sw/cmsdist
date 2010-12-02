### RPM cms wmcore WMCORE_0_6_0
## INITENV +PATH PYTHONPATH %i/lib

%define svnserver svn://svn.cern.ch/reps/CMSDMWM/WMCORE/tags/%{realversion}
Source: %svnserver?scheme=svn+ssh&strategy=export&module=WMCORE&output=/WMCORE.tar.gz

Requires: python py2-simplejson py2-sqlalchemy py2-httplib2

%prep
%setup -n WMCORE

%build

%install
make PREFIX=%i install
mkdir -p %i
cp -r * %i
chmod +x %i/lib/WMCore/WebTools/Root.py
mkdir -p %{i}/workdir

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

