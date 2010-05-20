### RPM cms overview 5.2.1

# This is a RPM spec file for building the Overview.  This is a very
# minimal SCRAM build area with highly reduced set of dependencies.
# Building Overview does not in fact require SCRAM at all, but this
# arrangment makes it easier for a developer with CMSSW work area.
# See DQM GUI spec file for more commentary on what goes on here.
%define cvsserver   cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define scram       $SCRAMV1_ROOT/bin/scram --arch %cmsplatf
%define cmssw       CMSSW_3_5_0
%define vcfg        V03-29-06
%define initenv     export ZZPATH=$PATH ZZLD_LIBRARY_PATH=$LD_LIBRARY_PATH ZZPYTHONPATH=$PYTHONPATH; %initenv_all

Source0: %{cvsserver}&strategy=checkout&module=config&export=config&tag=-r%{vcfg}&output=/config.tar.gz
Source1: %{cvsserver}&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&export=VisMonitoring/DQMServer&tag=-rR05-01-08&output=/DQMServer.tar.gz
Requires: cherrypy py2-cheetah yui py2-cx-oracle py2-pil py2-matplotlib overview-conf SCRAMV1

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
perl -p -i -e 's/DQMGUI\_ROOT/OVERVIEW_ROOT/g' %i/bin/visDQM*
for f in %i/bin/visDQM*; do
  mv $f $(echo $f | sed s/visDQM/ov/g)
done

(set -e; eval `scram runtime -sh`;
 export PYTHONPATH=%i/python${PYTHONPATH+":$PYTHONPATH"};
 for mod in %i/python/*.py; do
   python -c "import $(basename $mod | sed 's/\.py$//')"
 done)

# Post installation rules.  Relocate the various scripts.
# Relocate SCRAM-generated external link "database".
%post
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
