### RPM cms comp HG2011h


# This is a meta-package to group all cms comp services
# CMSWEB
Requires: frontend das dbs3 reqmon
Requires: dqmgui workqueue
Requires: dbs3-client crabserver crabclient crabcache
Requires: acdcserver
Requires: t0wmadatasvc dbs3-migration t0_reqmon reqmgr2 reqmgr2ms
Requires: cmsweb-analytics
Requires: popdbweb victorweb confdb exporters exitcodes
# Common
Requires: rotatelogs pystack py2-psutil wmcore-devtools
# Other
Requires: wmagent-dev condor crabtaskworker t0 couchdb15 crab-devtools
Requires: lifecycle-das
Requires: wmarchive
# Python3
BuildRequires: wmcorepy3-devtools
### List of services that are likely no longer needed
BuildRequires: DMWMMON-datasvc gitweb spacemon-client DCAFPilot compsec
### List of services being deprecated (or already deprecated), do not build them anymore!
#BuildRequires: filemover PHEDEX-combined-web PHEDEX-combined-agents PHEDEX-lifecycle
#BuildRequires: overview happyface sreadiness asyncstageout

%prep
%build
%install

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
