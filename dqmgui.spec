### RPM cms dqmgui 4.2.1b
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source0: %cvsserver&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&nocache=true&export=VisMonitoring/DQMServer&tag=-rV04-02-01&output=/VisMonitoring_DQMServer.tar.gz
Source1: %cvsserver&strategy=checkout&module=CMSSW/DQMServices/Core&nocache=true&export=DQMServices/Core&tag=-rV03-03-06&output=/DQMServices_Core.tar.gz
Source2: %cvsserver&strategy=checkout&module=CMSSW/DQMServices/Components&nocache=true&export=DQMServices/Components&tag=-rV03-03-03&output=/DQMServices_Components.tar.gz
Source3: %cvsserver&strategy=checkout&module=CMSSW/DQM/RenderPlugins&nocache=true&export=DQM/RenderPlugins&tag=-rV04-00-00&output=/DQM_RenderPlugins.tar.gz
Requires: cmssw cherrypy py2-cheetah yui py2-pysqlite py2-cx-oracle py2-pil py2-matplotlib

%prep
# Note on requiring "xsrc": using $CMSSW_VERSION/src in the setup
# stanzas with -n options won't work because then build rule will
# try to do a "cd" into $CMSSW_VERSION/src before the preamble has
# sourced the init scripts.  We use "xsrc" as a "constant-value"
# hack so we don't need to hard-code CMSSW version in this RPM.
rm -fr CMSSW_$VERSION xsrc
scram p CMSSW $CMSSW_VERSION
ln -s $CMSSW_VERSION/src xsrc
%setup -D -T -a 0 -c -n xsrc
%setup -D -T -a 1 -c -n xsrc
%setup -D -T -a 2 -c -n xsrc
%setup -D -T -a 3 -c -n xsrc

%build
# Build the code as a scram project area, then relocate it to more
# normal directories (%i/{bin,lib,python}).  Save the scram runtime
# environment plus extra externals for later use, but manipulate
# the scram environment to point to the installation directories.
# Avoid generating excess environment.
cd %_builddir/$CMSSW_VERSION/src
scram build %makeprocesses

mkdir -p %i/etc/profile.d
scram runtime -sh | grep -v SCRAMRT > %i/etc/profile.d/env.sh
scram runtime -csh | grep -v SCRAMRT > %i/etc/profile.d/env.csh
perl -p -i -e \
  "s<%_builddir/$CMSSW_VERSION/bin/%cmsplatf><%i/bin>g;
   s<%_builddir/$CMSSW_VERSION/(lib|module)/%cmsplatf><%i/lib>g;
   s<%_builddir/$CMSSW_VERSION/python><%i/python>g;
   s<%_builddir/$CMSSW_VERSION><%i>g;" \
  %i/etc/profile.d/env.sh %i/etc/profile.d/env.csh

for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`; do
  rootvar=`echo $tool | tr a-z- A-Z_`_ROOT
  eval root=\$$rootvar
  if [ X$root != X ]; then
    echo "[ X\$$rootvar != X ] || . $root/etc/profile.d/init.sh" >> %i/etc/profile.d/env.sh
    echo "[ X\$$rootvar != X ] || source $root/etc/profile.d/init.csh" >> %i/etc/profile.d/env.csh
  fi
done

%install
mkdir -p %i/etc %i/bin %i/lib %i/python
mv %_builddir/$CMSSW_VERSION/lib/%cmsplatf/*.{so,edm,ig}* %i/lib
mv %_builddir/$CMSSW_VERSION/bin/%cmsplatf/{vis*,DQMCollector} %i/bin
mv %_builddir/$CMSSW_VERSION/src/VisMonitoring/DQMServer/python/*.* %i/python

sed 's/^  //' > %i/etc/restart-collector << \END_OF_SCRIPT
  #!/bin/sh
  . %instroot/cmsset_default.sh
  . %i/etc/profile.d/env.sh
  killall -9 DQMCollector
  set -e
  mkdir -p $(dirname %instroot)/collector
  cd $(dirname %instroot)/collector
  [ ! -f collector.out ] || mv -f collector.out collector.out.$(date +%Y%m%d%H%M%S)
  DQMCollector > collector.out 2>&1 </dev/null &
END_OF_SCRIPT

sed 's/^  //' > %i/etc/archive-collector-logs << \END_OF_SCRIPT
  #!/bin/sh
  cd $(dirname %instroot)/collector
  for month in $(ls | fgrep collector.out. | sed 's/.*out.\(......\).*/\1/' | sort | uniq); do
    zip -rm collector-$month.zip collector.out.$month*
  done
END_OF_SCRIPT

sed 's/^  //' > %i/etc/purge-old-sessions << \END_OF_SCRIPT
  #!/bin/sh
  . %instroot/cmsset_default.sh
  . %i/etc/profile.d/env.sh
  visDQMPurgeSessions $(dirname %instroot)/gui/www/sessions
END_OF_SCRIPT

sed 's/^  //' > %i/etc/update-crontab << \END_OF_SCRIPT
  #!/bin/sh
  set -x
  (crontab -l | fgrep -v /dqmgui/; cat %i/etc/crontab) | crontab -
END_OF_SCRIPT

sed 's/^  //' > %i/etc/crontab << \END_OF_SCRIPT
  10 * * * * %i/etc/purge-old-sessions
  0 0 * * * %i/etc/restart-collector
  20 0 1 * * %i/etc/archive-collector-logs
END_OF_SCRIPT

chmod a+x %i/etc/restart-collector
chmod a+x %i/etc/archive-collector-logs
chmod a+x %i/etc/purge-old-sessions
chmod a+x %i/etc/update-crontab

%post
%{relocateConfig}etc/restart-collector
%{relocateConfig}etc/archive-collector-logs
%{relocateConfig}etc/purge-old-sessions
%{relocateConfig}etc/update-crontab
%{relocateConfig}etc/crontab
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
