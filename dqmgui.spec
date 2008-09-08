### RPM cms dqmgui 4.2.2b
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source0: %cvsserver&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&nocache=true&export=VisMonitoring/DQMServer&tag=-rV04-02-02&v=2&output=/VisMonitoring_DQMServer.tar.gz
Source1: %cvsserver&strategy=checkout&module=CMSSW/DQMServices/Core&nocache=true&export=DQMServices/Core&tag=-rV03-03-06&output=/DQMServices_Core.tar.gz
Source2: %cvsserver&strategy=checkout&module=CMSSW/DQMServices/Components&nocache=true&export=DQMServices/Components&tag=-rV03-03-03&output=/DQMServices_Components.tar.gz
Source3: %cvsserver&strategy=checkout&module=CMSSW/DQM/RenderPlugins&nocache=true&export=DQM/RenderPlugins&tag=-rV04-00-01&output=/DQM_RenderPlugins.tar.gz
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
  for opt in ${1+"$@"}; do
    case $opt in
      :* )  port= dir=$(echo $opt | sed 's/.*://') ;;
      *:* ) dir=$(echo $opt | sed 's/.*://')
            port=$(echo $opt | sed 's/:.*//') ;;
      * )  port= dir=$opt ;;
    esac

    mkdir -p $dir/collector
    cd $dir/collector
    [ ! -f collector.out ] || mv -f collector.out collector.out.$(date +%%Y%%m%%d%%H%%M%%S)
    DQMCollector ${port:+ --listen $port} > collector.out 2>&1 </dev/null &
  done
END_OF_SCRIPT

sed 's/^  //' > %i/etc/archive-collector-logs << \END_OF_SCRIPT
  #!/bin/sh
  for opt in ${1+"$@"}; do
    dir=$(echo $opt | sed 's/.*://')
    cd $dir/collector
    for month in $(ls | fgrep collector.out. | sed 's/.*out.\(......\).*/\1/' | sort | uniq); do
      zip -rm collector-$month.zip collector.out.$month*
    done
  done
END_OF_SCRIPT

sed 's/^  //' > %i/etc/purge-old-sessions << \END_OF_SCRIPT
  #!/bin/sh
  . %instroot/cmsset_default.sh
  . %i/etc/profile.d/env.sh
  for opt in ${1+"$@"}; do
    [ -d "$opt/gui/www/sessions" ] || continue
    visDQMPurgeSessions $opt/gui/www/sessions
  done
END_OF_SCRIPT

sed 's/^  //' > %i/etc/update-crontab << \END_OF_SCRIPT
  #!/bin/sh
  collector= defcollector=9090:$(dirname %instroot)
  purge= defpurge=$(dirname %instroot)
  while [ $# -gt 0 ]; do
    case $1 in
      --collector )
        collector="$collector $2"
        shift; shift ;;
      --purge )
        purge="$purge $2"
        shift; shift ;;
      * )
        echo "$(basename $0): unrecognised option $1" 1>&2
        exit 1 ;;
    esac
  done

  set -x
  (crontab -l | fgrep -v /dqmgui/;
   sed -e "s|#COLLECTOR|${collector:-$defcollector}|g" \
       -e "s|#PURGE|${purge:-$defpurge}|g" <%i/etc/crontab) |
  crontab -
END_OF_SCRIPT

sed 's/^  //' > %i/etc/crontab << \END_OF_SCRIPT
  5 */2 * * * %i/etc/purge-old-sessions #PURGE
  0 0 * * * %i/etc/restart-collector #COLLECTOR
  20 0 1 * * %i/etc/archive-collector-logs #COLLECTOR
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
