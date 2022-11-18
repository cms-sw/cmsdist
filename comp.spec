### RPM cms comp HG2212a


# This is a meta-package to group all cms comp services
# CMSWEB
Requires: frontend das dbs3 reqmon frontend8443
Requires: dqmgui workqueue
Requires: dbs3-client crabserver
Requires: acdcserver
Requires: t0wmadatasvc dbs3-migration t0_reqmon reqmgr2 reqmgr2ms
Requires: cmsweb-analytics
Requires: exporters exitcodes
# FIXME: remove these 3 PhEDEx specs from the building list for January/2021
Requires: PHEDEX-combined-web PHEDEX-combined-agents PHEDEX-lifecycle
# Common
Requires: rotatelogs wmcore-devtools
# Other
Requires: wmagent-dev condor crabtaskworker t0 crab-devtools
Requires: wmarchive
# Python3
BuildRequires: wmcorepy3-devtools wmagentpy3-dev
### List of services that are likely no longer needed, but nobody could confirm that..
BuildRequires: gitweb compsec couchdb
### List of obsolete services (or under deprecation), stop building them!
#BuildRequires: filemover PHEDEX-combined-web PHEDEX-combined-agents PHEDEX-lifecycle
#BuildRequires: overview happyface sreadiness lifecycle-das webtools
#BuildRequires: DCAFPilot DMWMMON-datasvc spacemon-client pystack

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
