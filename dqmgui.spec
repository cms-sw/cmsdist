### RPM cms dqmgui 4.2.0
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source0: %cvsserver&strategy=checkout&module=CMSSW/VisMonitoring/DQMServer&nocache=true&export=VisMonitoring/DQMServer&tag=-rV04-02-00&output=/VisMonitoring_DQMServer.tar.gz
Source1: %cvsserver&strategy=checkout&module=CMSSW/DQMServices/Core&nocache=true&export=DQMServices/Core&tag=-rV03-03-04&output=/DQMServices_Core.tar.gz
Source2: %cvsserver&strategy=checkout&module=CMSSW/DQMServices/Components&nocache=true&export=DQMServices/Components&tag=-rV03-03-03&output=/DQMServices_Components.tar.gz
Source3: %cvsserver&strategy=checkout&module=CMSSW/DQM/RenderPlugins&nocache=true&export=DQM/RenderPlugins&tag=-rV04-00-00&output=/DQM_RenderPlugins.tar.gz
Requires: cmssw cms-common cherrypy py2-cheetah yui py2-pysqlite py2-cx-oracle py2-pil py2-matplotlib

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
mv %_builddir/$CMSSW_VERSION/bin/%cmsplatf/vis* %i/bin
mv %_builddir/$CMSSW_VERSION/src/VisMonitoring/DQMServer/python/*.* %i/python

%post
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
