### RPM cms overview 4.6.1

%define cvsserver   cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define initenv     export ZZPATH=$PATH ZZLD_LIBRARY_PATH=$LD_LIBRARY_PATH ZZPYTHONPATH=$PYTHONPATH; %initenv_all

Source0: %{cvsserver}&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&export=VisMonitoring/DQMServer&tag=-rR04-06-01&output=/DQMServer.tar.gz
Requires: cherrypy py2-cheetah yui py2-pysqlite py2-cx-oracle py2-pil py2-matplotlib

%prep
%setup -c -T -n src -a 0
tar -jcvf ../distsrc.tar.bz2 .

%build
for f in */*/scripts/visDQM*; do
  mv $f $(echo $f | sed s/visDQM/ov/g)
done

%install
# Relocate code to normal %i/{lib,bin,python} directories. Save the
# runtime environment needed for later use, but avoid excess values.
mkdir -p %i/etc/profile.d %i/{x,}bin %i/{x,}lib %i/{x,}python %i/data
cp -p %_builddir/distsrc.tar.bz2 %i/data
export PYTHONPATH=%i/python${PYTHONPATH+":$PYTHONPATH"};

cd %_builddir/src
for d in */*; do
  if [ -d $d/python ]; then
    cp -p $d/python/*.{py,js,css,gif,png,tmpl} %i/python
    rm -f %i/python/GuiDQM.py
  fi

  for f in $d/scripts/*; do
    if [ -f $f ]; then cp -p $f %i/bin; fi
  done
done

for mod in %i/python/*.py; do
  python -c "import $(basename $mod | sed 's/\.py$//')"
done

# Now generate server start-up environment. Eliminate non-existent and
# duplicate path components and convert back to format that only adds to
# user's one, not one that uses RPM-builder's environment. Finally munge
# in patch directories.
for p in PATH LD_LIBRARY_PATH PYTHONPATH; do
  for z in "" ZZ; do
    eval export $z$p=$(perl -e 'print join(":", grep($_ && -d $_ && scalar(@{[<$_/*>]}) > 0, split(/:/,$ENV{'$z$p'})))')
  done
done
perl -w -i -e \
  'open(SH, "> %i/etc/profile.d/env.sh") || die;
   open(CSH, "> %i/etc/profile.d/env.csh") || die;
   $ENV{PATH} = "%i/xbin:%i/bin:$ENV{PATH}";
   $ENV{LD_LIBRARY_PATH} = "%i/xlib:%i/lib:$ENV{LD_LIBRARY_PATH}";
   $ENV{PYTHONPATH} = "%i/xpython:%i/python:$ENV{PYTHONPATH}";
   foreach $p ("PATH", "LD_LIBRARY_PATH", "PYTHONPATH") {
     %%seen = ();
     $ENV{"ZZ$p"} = join(":", grep($_ && -d $_ && scalar(@{[<$_/*>]}) > 0, split(/:/,$ENV{"ZZ$p"})));
     $ENV{"$p"} = join(":", grep($_ && -d $_ && scalar(@{[<$_/*>]}) > 0, split(/:/,$ENV{"$p"})));
     $ENV{$p} =~ s<([ :=])$ENV{"ZZ$p"}([ :;"]|$)><$1\${$p}$2>g if $ENV{"ZZ$p"};
     $ENV{$p} = join(":", map { ($seen{$_} ? () : do { $seen{$_} = 1; ($_) }) } split(/:/, $ENV{$p}));
     print SH "export $p=$ENV{$p};\n";
     print CSH "setenv $p $ENV{$p};\n";
   }
   print SH "export YUI_ROOT=$ENV{YUI_ROOT};\n";
   print CSH "setenv YUI_ROOT $ENV{YUI_ROOT};\n";
   close(SH); close(CSH);'

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
