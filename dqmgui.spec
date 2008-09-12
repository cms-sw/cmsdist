### RPM cms dqmgui 4.2.4
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source0: %cvsserver&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&nocache=true&export=VisMonitoring/DQMServer&tag=-rV04-02-04&output=/VisMonitoring_DQMServer.tar.gz
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

(echo "export PATH=%i/xbin:\$PATH;"
 echo "export PYTHONPATH=%i/xlib:%i/xpython:\$PYTHONPATH;"
 echo "export LD_LIBRARY_PATH=%i/xlib:\$LD_LIBRARY_PATH;"
 echo "export YUI_ROOT='$YUI_ROOT';"
 echo "export DQM_CMSSW_VERSION='$CMSSW_VERSION';") >> %i/etc/profile.d/env.sh

(echo "setenv PATH %i/xbin:\$PATH;"
 echo "setenv PYTHONPATH %i/xlib:%i/xpython:\$PYTHONPATH;"
 echo "setenv LD_LIBRARY_PATH %i/xlib:\$LD_LIBRARY_PATH;"
 echo "setenv YUI_ROOT '$YUI_ROOT';"
 echo "setenv DQM_CMSSW_VERSION '$CMSSW_VERSION';") >> %i/etc/profile.d/env.csh

%install
mkdir -p %i/etc %i/{,x}bin %i/{,x}lib %i/{,x}python
cp -p %_builddir/$CMSSW_VERSION/lib/%cmsplatf/*.{so,edm,ig}* %i/lib
cp -p %_builddir/$CMSSW_VERSION/bin/%cmsplatf/{vis*,DQMCollector} %i/bin
cp -p %_builddir/$CMSSW_VERSION/src/VisMonitoring/DQMServer/python/*.* %i/python

(echo '#!/bin/sh';
 echo 'doit= shopt=-ex'
 echo 'while [ $# -gt 0 ]; do'
 echo ' case $1 in'
 echo '  -n ) doit=echo shopt=-e; shift ;;'
 echo '  * )  echo "$0: unrecognised parameter: $1" 1>&2; exit 1 ;;'
 echo ' esac'
 echo 'done'
 echo 'set $shopt'
 cd %_builddir/$CMSSW_VERSION/src
 for f in */*/CVS/Tag; do
   [ -f $f ] || continue
   tag=$(cat $f | sed 's/^N//')
   pkg=$(echo $f | sed 's|/CVS/Tag||')
   echo "\$doit cvs -Q co -r $tag $pkg"
 done) > %i/bin/visDQMDistSource

sed 's/^  //' > %i/bin/visDQMDistPatch << \END_OF_SCRIPT
  #!/bin/sh

  if [ X"$CMSSW_BASE" = X%i ]; then
    unset CMSSW_BASE
  fi

  if [ X"$CMSSW_BASE" = X ]; then
    echo "warning: local scram runtime environment not set, sourcing now" 1>&2
    eval `scram runtime -sh`
  fi

  if [ X"$CMSSW_BASE" = X ] || [ X"$SCRAM_ARCH" = X ] || \
     [ ! -f "$CMSSW_BASE/lib/$SCRAM_ARCH/.iglets" ]; then
    echo "error: could not locate local scram developer area, exiting" 1>&2
    exit 1;
  fi

  set -e
  rm -fr %i/x{lib,bin,python}/{*,.??*}

  echo "copying $CMSSW_BASE/lib/$SCRAM_ARCH into %i/xlib"
  (cd $CMSSW_BASE/lib/$SCRAM_ARCH && tar -cf - .) | (cd %i/xlib && tar -xvvf -)

  echo "copying $CMSSW_BASE/bin/$SCRAM_ARCH into %i/xbin"
  (cd $CMSSW_BASE/bin/$SCRAM_ARCH && tar -cf - .) | (cd %i/xbin && tar -xvvf -)

  echo "copying $CMSSW_BASE/src/VisMonitoring/DQMServer/python into %i/xpython"
  (cd $CMSSW_BASE/src/VisMonitoring/DQMServer/python && tar -cf - *.*) | (cd %i/xpython && tar -xvvf -)
  exit 0
END_OF_SCRIPT

sed 's/^  //' > %i/bin/visDQMDistUnpatch << \END_OF_SCRIPT
  #!/bin/sh
  echo "removing local overrides from %i"
  rm -fr %i/x{lib,bin,python}/{*,.??*}
  exit 0
END_OF_SCRIPT

sed 's/^  //' > %i/etc/restart-collector << \END_OF_SCRIPT
  #!/bin/sh
  . %instroot/cmsset_default.sh
  . %i/etc/profile.d/env.sh
  killall -9 DQMCollector
  set -e
  for opt; do
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
  for opt; do
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
  for opt; do
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

chmod a+x %i/bin/visDQMDist*
chmod a+x %i/etc/*-*

%post
%{relocateConfig}bin/visDQMDist*
%{relocateConfig}etc/*-*
%{relocateConfig}etc/crontab
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
