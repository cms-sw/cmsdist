### RPM cms comp HG1410e

# This is a meta-package to group all cms comp services
# CMSWEB
Requires: frontend das dbs3 filemover sitedb couchdb bigcouch reqmon
Requires: PHEDEX-combined-web stagemanager reqmgr dqmgui overview workqueue
Requires: dbs3-client stagemanager-agent crabserver crabclient crabcache
Requires: DMWMMON-datasvc alertscollector acdcserver gitweb
Requires: asyncstageout t0wmadatasvc dbs3-migration t0_reqmon reqmgr2
Requires: cmsweb-analytics py2-geoip py2-adns py2-netaddr valgrind igprof yui3
# CMSFOMON
Requires: crabhb happyface sreadiness mechanize
# Common
Requires: rotatelogs pystack py2-psutil wmcore-devtools
# Other
Requires: wmagent-dev condor crabtaskworker t0 couchdb15
Requires: PHEDEX-combined-agents PHEDEX-lifecycle lifecycle-das

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
