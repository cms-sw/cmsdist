### RPM cms overview 5.1.5

# This is a RPM spec file for building the Overview.  This is a very
# minimal SCRAM build area with highly reduced set of dependencies.
# Building Overview does not in fact require SCRAM at all, but this
# arrangment makes it easier for a developer with CMSSW work area.
# See DQM GUI spec file for more commentary on what goes on here.
%define cvsserver   cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define scram       $SCRAMV1_ROOT/bin/scram --arch %cmsplatf
%define cmssw       CMSSW_3_3_1
%define vcfg        V03-26-04-01
%define initenv     export ZZPATH=$PATH ZZLD_LIBRARY_PATH=$LD_LIBRARY_PATH ZZPYTHONPATH=$PYTHONPATH; %initenv_all

Source0: %{cvsserver}&strategy=checkout&module=config&export=config&tag=-r%{vcfg}&output=/config.tar.gz
Source1: %{cvsserver}&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&export=VisMonitoring/DQMServer&tag=-rR05-01-05&output=/DQMServer.tar.gz
Requires: cherrypy py2-cheetah yui py2-cx-oracle py2-pil py2-matplotlib overview-conf SCRAMV1 dbs-client

# Set up minimal SCRAM project build area with our sources.
%prep
rm -fr %_builddir/{config,src,THE_BUILD}
%setup    -T -b 0 -n config
%setup -c -T -a 1 -n src

cd %_builddir
rm -fr src/Vis*/*/{src,bin,interface,plugins,test}
tar -jcvf distsrc.tar.bz2 -C src .

config/updateConfig.pl -p CMSSW -v THE_BUILD -s $SCRAMV1_VERSION -t ${OVERVIEW_CONF_ROOT}
%scram project -d $PWD -b config/bootsrc.xml </dev/null

%build
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
(%scram build -v -f %makeprocesses </dev/null) || { %scram build outputlog </dev/null && false; }

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
 echo "export OVERVIEW_ROOT='%i';"
 echo "export OVERVIEW_CMSSW_VERSION='%{cmssw}';") >> %i/etc/profile.d/env.sh

(echo "setenv PATH %i/xbin:\$PATH;"
 echo "setenv PYTHONPATH %i/xlib:%i/xpython:\$PYTHONPATH;"
 echo "setenv LD_LIBRARY_PATH %i/xlib:\$LD_LIBRARY_PATH;"
 echo "setenv YUI_ROOT '$YUI_ROOT';"
 echo "setenv OVERVIEW_ROOT '%i';"
 echo "setenv OVERVIEW_CMSSW_VERSION '%{cmssw}';") >> %i/etc/profile.d/env.csh

# Install the project files.  Copies from SCRAM area to final install
# area.  Creates scripts to patch and unpatch the server area from a
# local SCRAM developer area.  Creates scripts for server management.
# Usage at https://twiki.cern.ch/twiki/bin/view/CMS/DQMTest and
# https://twiki.cern.ch/twiki//bin/view/CMS/DQMGuiProduction.
%install
mkdir -p %i/etc/profile.d %i/etc/scramconfig %i/external %i/{,x}bin %i/{,x}lib %i/{,x}python %i/data
cp -p %_builddir/distsrc.tar.bz2 %i/data
cp -p %_builddir/THE_BUILD/bin/%cmsplatf/* %i/bin
cp -p %_builddir/THE_BUILD/src/VisMonitoring/DQMServer/python/*.* %i/python
tar -C %_builddir/THE_BUILD/external/%cmsplatf/lib -cf - . | tar -C %i/external -xvvf -
cp -p %_builddir/THE_BUILD/config/toolbox/%cmsplatf/tools/selected/*.xml %i/etc/scramconfig
rm -f %i/python/GuiDQM.py

# Rename executable scripts.
for f in %i/bin/visDQM*; do
  mv $f $(echo $f | sed s/visDQM/ov/g)
done

(set -e; eval `scram runtime -sh`;
 export PYTHONPATH=%i/python${PYTHONPATH+":$PYTHONPATH"};
 for mod in %i/python/*.py; do
   python -c "import $(basename $mod | sed 's/\.py$//')"
 done)

# Script to record what sources went into this package so user can
# check them out conveniently.
sed 's/^  //' > %i/bin/ovDistSource << \END_OF_SCRIPT
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

# Script to update SCRAM tool definitions in CMSSW to our versions.
sed 's/^  //' > %i/bin/ovDistTools << \END_OF_SCRIPT
  #!/bin/sh
  [ X"$CMSSW_BASE" = X ] && { echo '$CMSSW_BASE not set'; exit 1; }
  [ X"$SCRAM_ARCH" = X ] && { echo '$SCRAM_ARCH not set'; exit 1; }

  set -e
  for tool in %i/etc/scramconfig/*.xml; do
   toolname=$(basename $tool | sed 's/\.xml$//')
   (set -x; scram tool remove $toolname)
   cp -p $tool $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected
   (set -x; scram setup -f $tool $toolname)
  done
END_OF_SCRIPT

# Script to patch the server from the local developer area.  The user's
# stuff goes into xbin/xlib/xpython directories, which are in front of
# the server's own bin/lib/python directories.  So anything in x* will
# be picked up in preference to the server-distributed files.
sed 's/^  //' > %i/bin/ovDistPatch << \END_OF_SCRIPT
  #!/bin/sh

  if [ X"$CMSSW_BASE" = X ]; then
    echo "scram runtime not set, will use one from $PWD" 1>&2
    eval `scram runtime -sh`
  fi

  if [ X"$CMSSW_BASE" = X ] || [ X"$SCRAM_ARCH" = X ] || \
     [ ! -f "$CMSSW_BASE/src/VisMonitoring/DQMServer/python/GuiCore.py" ]; then
    echo "error: could not locate local scram developer area, exiting" 1>&2
    exit 1;
  fi

  set -e
  rm -fr %i/x{lib,bin,python}/{*,.??*}

  echo "copying $CMSSW_BASE/lib/$SCRAM_ARCH into %i/xlib"
  (cd $CMSSW_BASE/lib/$SCRAM_ARCH && tar -cf - .) | (cd %i/xlib && tar -xf -)

  echo "copying $CMSSW_BASE/bin/$SCRAM_ARCH into %i/xbin"
  (cd $CMSSW_BASE/bin/$SCRAM_ARCH && tar -cf - .) | (cd %i/xbin && tar -xf -)

  echo "copying $CMSSW_BASE/src/VisMonitoring/DQMServer/python into %i/xpython"
  (cd $CMSSW_BASE/src/VisMonitoring/DQMServer/python && tar -cf - *.*) | (cd %i/xpython && tar -xf -)

  echo "renaming utility scripts"
  for f in %i/xbin/visDQM*; do
    mv $f $(echo $f | sed s/visDQM/ov/g)
  done
  exit 0
END_OF_SCRIPT

# Script to unpatch the server area.  Simply clears out xbin/xlib/xpython
# so the server will then pick up the files distributed with the RPM.
sed 's/^  //' > %i/bin/ovDistUnpatch << \END_OF_SCRIPT
  #!/bin/sh
  echo "removing local overrides from %i"
  rm -fr %i/x{lib,bin,python}/{*,.??*}
  exit 0
END_OF_SCRIPT

# CRON script to purge sessions abandoned by users.
sed 's/^  //' > %i/etc/purge-old-sessions << \END_OF_SCRIPT
  #!/bin/sh
  . %instroot/cmsset_default.sh
  . %i/etc/profile.d/env.sh
  for opt; do
    [ -d "$opt/gui/www/sessions" ] || continue
    ovPurgeSessions $opt/gui/www/sessions
  done
END_OF_SCRIPT

# Utility script to update CRONTAB entries to this server version.
# Accounts for changes in the server configurations.  For details
# of use see DQMGuiProduction twiki page.
sed 's/^  //' > %i/etc/update-crontab << \END_OF_SCRIPT
  #!/bin/sh
  purge= defpurge=$(dirname %instroot)
  while [ $# -gt 0 ]; do
    case $1 in
      --purge )
        purge="$purge $2"
        shift; shift ;;
      * )
        echo "$(basename $0): unrecognised option $1" 1>&2
        exit 1 ;;
    esac
  done

  set -x
  (crontab -l | fgrep -v /overview/;
   sed -e "s|#PURGE|${purge:-$defpurge}|g" <%i/etc/crontab) |
  crontab -
END_OF_SCRIPT

# CRONTAB entries for this server.  This will be modified by the
# update-crontab script and merged to other crontab rules.
sed 's/^  //' > %i/etc/crontab << \END_OF_SCRIPT
  5 */2 * * * %i/etc/purge-old-sessions #PURGE
END_OF_SCRIPT

chmod a+x %i/bin/ovDist*
chmod a+x %i/etc/*-*

# Post installation rules.  Relocate the various scripts.
# Relocate SCRAM-generated external link "database".
%post
%{relocateConfig}bin/ovDist*
%{relocateConfig}etc/*-*
%{relocateConfig}etc/crontab
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
%{relocateConfig}etc/scramconfig/*.xml
perl -w -e '
  ($oldroot, $newroot, @files) = @ARGV;
  foreach $f (@files) {
    next if !defined($old = readlink $f);
    ($new = $old) =~ s|\Q$oldroot\E|$newroot|;
    if ($new ne $old) { unlink($f); symlink($new, $f); }
  }' %instroot $RPM_INSTALL_PREFIX $RPM_INSTALL_PREFIX/%pkgrel/external/*
