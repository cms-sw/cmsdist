### RPM cms dqmgui 4.6.0

# This is a RPM spec file for building the DQM GUI.  This effectively
# builds a sliced version of CMSSW with some updated and added code,
# and highly reduced dependencies.  The result is built using SCRAM
# just like CMSSW, and SCRAM is used to record the suitable run-time
# environment, but the build product is a "bare" install area with
# no memory of SCRAM.  There's support for "patching" the server from
# a developer SCRAM build area.  In addition this spec file packages
# server admin scripts that are highly dependent on install location.

# Basic variables for source.  "cmssw" is the underlying CMSSW version
# and "vcfg" is the SCRAM configuration version that goes with it: get
# CMSDIST with tag %cmssw, then take version from cms-scram-build.file.
%define cvsserver   cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define scram       $SCRAMV1_ROOT/bin/scram --arch %cmsplatf
%define cmssw       CMSSW_2_2_10
%define vcfg        V03-17-02
%define initenv     export ZZPATH=$PATH ZZLD_LIBRARY_PATH=$LD_LIBRARY_PATH ZZPYTHONPATH=$PYTHONPATH; %initenv_all

# Sources that go into this package.  To avoid listing every package
# here we take entire subsystems then later select what we want.
Source0: %{cvsserver}&strategy=checkout&module=config&export=config&tag=-r%{vcfg}&output=/config.tar.gz
Source1: %{cvsserver}&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&export=VisMonitoring/DQMServer&tag=-rR04-06-00&output=/DQMServer.tar.gz
Source2: %{cvsserver}&strategy=checkout&module=CMSSW/Iguana/Utilities&export=Iguana/Utilities&tag=-rV03-00-09-01&output=/IgUtils.tar.gz
Source3: %{cvsserver}&strategy=checkout&module=CMSSW/DQMServices/Core&export=DQMServices/Core&tag=-rV03-09-03&output=/DQMCore.tar.gz
Requires: cherrypy py2-cheetah yui py2-pysqlite py2-cx-oracle py2-pil py2-matplotlib dqmgui-conf SCRAMV1

# Set up the project build area: extract sources, bootstrap the SCRAM
# build area with them.  Filters out the sources we actually want.
# Removes all tests and some EDM binaries to reduce dependencies on
# otherwise unnecessary software.
%prep
rm -fr %_builddir/{config,src,THE_BUILD}
%setup    -T -b 0 -n config
%setup -c -T -a 1 -n src
%setup -D -T -a 2 -n src
%setup -D -T -a 3 -n src

cd %_builddir
rm -fr src/DQM*/*/{test,plugins}
find src/DQM*/* -name BuildFile | xargs perl -n -i -e '/WITHOUT_CMS/ && s/=0/=1/; /FWCore/ || print'
tar -jcvf distsrc.tar.bz2 -C src .

config/updateConfig.pl -p CMSSW -v THE_BUILD -s $SCRAMV1_VERSION -t ${DQMGUI_CONF_ROOT}
%scram project -d $PWD -b config/bootsrc.xml

# Build the code as a scram project area, then relocate it to more
# normal directories (%i/{bin,lib,python}).  Save the scram runtime
# environment plus extra externals for later use, but manipulate
# the scram environment to point to the installation directories.
# Avoid generating excess environment.
%build
cd %_builddir/THE_BUILD/src
export BUILD_LOG=yes
export SCRAM_NOPLUGINREFRESH=yes
export SCRAM_NOLOADCHECK=true
export SCRAM_NOSYMCHECK=true
(%scram build -v -f %makeprocesses </dev/null) || { %scram build outputlog && false; }

# Now clean up environment.  First eliminate non-existent directories
# from the paths.  Then capture the SCRAM run-time environment, and
# eliminate duplicate path components (from cmsbuild vs. scram), and
# convert it back to a format that is additive to the user environment
# (you want the init script to modify your $PATH, not to change it to
# mine, right!?).  Finally munge SCRAM directories to finall install
# area directories.
mkdir -p %i/etc/profile.d
for p in PATH LD_LIBRARY_PATH PYTHONPATH; do
  for z in "" ZZ; do
    eval export $z$p=$(perl -e 'print join(":", grep($_ && -d $_ && scalar(@{[<$_/*>]}) > 0, split(/:/,$ENV{'$z$p'})))')
  done
done
removeenv='LOCALRT|CMSSW_(RELEASE_)*(BASE|VERSION|(FWLITE|SEARCH)_[A-Z_]*)|(COIN|IGUANA|SEAL)_[A-Z_]*'
scram runtime -sh | grep -v SCRAMRT | egrep -v "^export ($removeenv)=" > %i/etc/profile.d/env.sh
scram runtime -csh | grep -v SCRAMRT | egrep -v "^setenv ($removeenv) " > %i/etc/profile.d/env.csh
perl -w -i -p -e \
  'BEGIN {
     %%linked = map { s|/+[^/]+$||; ($_ => 1) }
                grep(defined $_, map { readlink $_ }
                     <%_builddir/THE_BUILD/external/%cmsplatf/lib/*>);
   }
   foreach $dir (keys %%linked) { s<:$dir([ :;"]|$)><$1>g; }
   foreach $p ("PATH", "LD_LIBRARY_PATH", "PYTHONPATH") {
     s<([ :=])$ENV{"ZZ$p"}([ :;"]|$)><$1\${$p}$2>g if $ENV{"ZZ$p"};
   }
   s<:'"$SCRAMV1_ROOT"'/[a-z]+:><:>g;
   s<:%instroot/common:><:>g;
   s<%_builddir/THE_BUILD/bin/%cmsplatf><%i/bin>g;
   s<%_builddir/THE_BUILD/(lib|module)/%cmsplatf><%i/lib>g;
   s<%_builddir/THE_BUILD/external/%cmsplatf/lib><%i/external>g;
   s<%_builddir/THE_BUILD/python><%i/python>g;
   s<%_builddir/THE_BUILD><%i>g;' \
  %i/etc/profile.d/env.sh %i/etc/profile.d/env.csh

(echo "export PATH=%i/xbin:\$PATH;"
 echo "export PYTHONPATH=%i/xlib:%i/xpython:\$PYTHONPATH;"
 echo "export LD_LIBRARY_PATH=%i/xlib:\$LD_LIBRARY_PATH;"
 echo "export YUI_ROOT='$YUI_ROOT';"
 echo "export DQMGUI_ROOT='%i';"
 echo "export DQMGUI_CMSSW_VERSION='%{cmssw}';") >> %i/etc/profile.d/env.sh

(echo "setenv PATH %i/xbin:\$PATH;"
 echo "setenv PYTHONPATH %i/xlib:%i/xpython:\$PYTHONPATH;"
 echo "setenv LD_LIBRARY_PATH %i/xlib:\$LD_LIBRARY_PATH;"
 echo "setenv YUI_ROOT '$YUI_ROOT';"
 echo "setenv DQMGUI_ROOT '%i';"
 echo "setenv DQMGUI_CMSSW_VERSION '%{cmssw}';") >> %i/etc/profile.d/env.csh

# Install the project files.  Copies from SCRAM area to final install
# area.  Creates scripts to patch and unpatch the server area from a
# local SCRAM developer area.  Creates scripts for server management.
# Usage at https://twiki.cern.ch/twiki/bin/view/CMS/DQMTest and
# https://twiki.cern.ch/twiki//bin/view/CMS/DQMGuiProduction.
%install
mkdir -p %i/etc %i/external %i/{,x}bin %i/{,x}lib %i/{,x}python %i/{,x}include %i/data
cp -p %_builddir/distsrc.tar.bz2 %i/data
cp -p %_builddir/THE_BUILD/lib/%cmsplatf/*.so %i/lib
cp -p %_builddir/THE_BUILD/bin/%cmsplatf/*DQM* %i/bin
cp -p %_builddir/THE_BUILD/src/VisMonitoring/DQMServer/python/*.* %i/python
cp -p %_builddir/THE_BUILD/src/VisMonitoring/DQMServer/config/makefile %i/etc
tar -C %_builddir/THE_BUILD/src -cf - */*/interface/*.h | tar -C %i/include -xvvf -
tar -C %_builddir/THE_BUILD/include/%cmsplatf -cf - . | tar -C %i/include -xvvf -
tar -C %_builddir/THE_BUILD/external/%cmsplatf/lib -cf - . | tar -C %i/external -xvvf -

# Script to record what sources went into this package so user can
# check them out conveniently.
sed 's/^  //' > %i/bin/visDQMDistSource << \END_OF_SCRIPT
  #!/bin/sh
  doit= shopt=-ex cvs=${CVSROOT:-":pserver:anonymous@cmscvs.cern.ch:/cvs/CMSSW"}
  while [ $# -gt 0 ]; do
    case $1 in
      -n ) doit=echo shopt=-e; shift ;;
       * ) echo "$0: unrecognised parameter: $1" 1>&2; exit 1 ;;
    esac
  done
  set $shopt
  $doit tar -jxf %i/data/distsrc.tar.bz2
  tar -jtf %i/data/distsrc.tar.bz2 '*/CVS/Root' |
    xargs $doit sed -i -e "s|.*|$cvs|"
END_OF_SCRIPT

# Script to patch the server from the local developer area.  The user's
# stuff goes into xbin/xlib/xpython directories, which are in front of
# the server's own bin/lib/python directories.  So anything in x* will
# be picked up in preference to the server-distributed files.
sed 's/^  //' > %i/bin/visDQMDistPatch << \END_OF_SCRIPT
  #!/bin/sh

  if [ X"$CMSSW_BASE" = X ]; then
    echo "scram runtime not set, will use one from $PWD" 1>&2
    eval `scram runtime -sh`
  fi

  if [ X"$CMSSW_BASE" = X ] || [ X"$SCRAM_ARCH" = X ] || \
     [ ! -f "$CMSSW_BASE/lib/$SCRAM_ARCH/libVisDQMServer.so" ]; then
    echo "error: could not locate local scram developer area, exiting" 1>&2
    exit 1;
  fi

  set -e
  rm -fr %i/x{lib,bin,python,include}/{*,.??*}

  echo "copying $CMSSW_BASE/lib/$SCRAM_ARCH into %i/xlib"
  (cd $CMSSW_BASE/lib/$SCRAM_ARCH && tar -cf - .) | (cd %i/xlib && tar -xf -)

  echo "copying $CMSSW_BASE/bin/$SCRAM_ARCH into %i/xbin"
  (cd $CMSSW_BASE/bin/$SCRAM_ARCH && tar -cf - .) | (cd %i/xbin && tar -xf -)

  echo "copying $CMSSW_BASE/src/VisMonitoring/DQMServer/python into %i/xpython"
  (cd $CMSSW_BASE/src/VisMonitoring/DQMServer/python && tar -cf - *.*) | (cd %i/xpython && tar -xf -)

  echo "copying $CMSSW_BASE/include/$SCRAM_ARCH into %i/xinclude"
  (cd $CMSSW_BASE/include/$SCRAM_ARCH && tar -cf - .) | (cd %i/xinclude && tar -xf -)

  echo "copying $CMSSW_BASE/src/*/*/interface/*.h into %i/xinclude"
  (cd $CMSSW_BASE/src && tar -cf - */*/interface/*.h) | (cd %i/xinclude && tar -xf -)
  exit 0
END_OF_SCRIPT

# Script to unpatch the server area.  Simply clears out xbin/xlib/xpython
# so the server will then pick up the files distributed with the RPM.
sed 's/^  //' > %i/bin/visDQMDistUnpatch << \END_OF_SCRIPT
  #!/bin/sh
  echo "removing local overrides from %i"
  rm -fr %i/x{lib,bin,python,include}/{*,.??*}
  exit 0
END_OF_SCRIPT

# CRON script to restart the DQM collector(s).
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

# CRON script to archive collector longs in monthly zip files.
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

# CRON script to purge sessions abandoned by users.
sed 's/^  //' > %i/etc/purge-old-sessions << \END_OF_SCRIPT
  #!/bin/sh
  . %instroot/cmsset_default.sh
  . %i/etc/profile.d/env.sh
  for opt; do
    [ -d "$opt/gui/www/sessions" ] || continue
    visDQMPurgeSessions $opt/gui/www/sessions
  done
END_OF_SCRIPT

# Utility script to update CRONTAB entries to this server version.
# Accounts for changes in the server configurations.  For details
# of use see DQMGuiProduction twiki page.
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

# CRONTAB entries for this server.  This will be modified by the
# update-crontab script and merged to other crontab rules.
sed 's/^  //' > %i/etc/crontab << \END_OF_SCRIPT
  5 */2 * * * %i/etc/purge-old-sessions #PURGE
  0 0 * * * %i/etc/restart-collector #COLLECTOR
  20 0 1 * * %i/etc/archive-collector-logs #COLLECTOR
END_OF_SCRIPT

chmod a+x %i/bin/visDQMDist*
chmod a+x %i/etc/*-*

# Post installation rules.  Relocate the various scripts.
# Relocate SCRAM-generated external link "database".
%post
%{relocateConfig}bin/visDQMDist*
%{relocateConfig}etc/*-*
%{relocateConfig}etc/crontab
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
perl -w -e '
  ($oldroot, $newroot, @files) = @ARGV;
  foreach $f (@files) {
    next if !defined($old = readlink $f);
    ($new = $old) =~ s|\Q$oldroot\E|$newroot|;
    if ($new ne $old) { unlink($f); symlink($new, $f); }
  }' %instroot $RPM_INSTALL_PREFIX $RPM_INSTALL_PREFIX/%pkgrel/external/*
