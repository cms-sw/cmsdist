### RPM cms apache2-conf 3.0
#%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
#Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rSERVER_CONF_2_9&output=/config.tar.gz
Source: http://cmsmac01.cern.ch/~lat/exports/apacheconf.tar.gz
Requires: apache2

%prep
%setup -c -n conf

%build

%install
mkdir -p %i/{bin,etc/env.d,etc/profile.d}
mv %_builddir/conf/mkserver %i/bin/
mv %_builddir/conf/* %i/
ln -sf ../profile.d/init.sh %i/etc/env.d/00-core-server.sh

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
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
%{relocateConfig}etc/profile.d/dependencies.*sh
