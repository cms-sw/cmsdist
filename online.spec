### RPM cms online CMSSW_1_7_0_ONLINE
## IMPORT configurations 
Provides: /bin/zsh
Requires: online-tool-conf python
Requires: SCRAMV1
%define cmssw_release   %(perl -e '$_="%v"; s/_ONLINE//; print;')
%define ucprojname  CMSSW
%define lcprojname  cmssw

%define buildtarget     release-build
%define saveDeps        yes
%define cvsproj         %cvsprojuc
%define srctree		src

#%define scram_xml   .xml
%define scram_xml   %{nil}
%define scramcmd    scramv1  -arch %{cmsplatf}

# NR: allow to change tarball names, otherwise old distributions
# are fetched from the apt SOURCE repository. 

%if "%{?configtar:set}" != "set"
%define configtar	config.tar.gz
%endif

%define cmsswsrc http://cmsrep.cern.ch/cms/cpt/Software/download/cms/SOURCES/cms/cmssw/%{cmssw_release}
# For partial releases re-using CMSSW sources:
%if "%{?cmsswsrc:set}" == "set"
Source0: %{cmsswsrc}/config.tar.gz
Source1: %{cmsswsrc}/src.tar.gz
%endif

# List of packages to bootstrap for partial builds:
Source2: online_build_set
Source3: cmssw-tool
Source4: findDependencies.pl

%prep
rm -rf config
rm -rf %{srctree}
# Create a SCRAM project area, but using the already extracted
# sources.  In other words, pick up the files from the project config
# area, but munge all instances of <base url="cvs:*"> into a local
# reference so SCRAM won't try to download stuff from the network.

%setup -T -b 0 -n config
%setup -D -T -b 1 -n %{srctree}
#%setup -D -T -a 2 -n %{srctree}

# Remove plugins that only include tests, which we do not build:
rm -rf %_builddir/src/FWCore/Framework/plugins
rm -rf %_builddir/src/RecoVertex/KalmanVertexFit/plugins
rm -rf %_builddir/src/Alignment/CommonAlignmentMonitor/plugins

touch %_builddir/config/%{ucprojname}_ignore.file
for file in `ls %_builddir/config/%{ucprojname}_*.file | grep -v  '/%{ucprojname}_ignore.file$' | sed 's|.*/%{ucprojname}_||;s|.file$||'`; do
  sed 's|@PROJECT_NAME@|%ucprojname|g;s|@PROJECT_VERSION@|%v|g;s|@PROJECT_BUILD_PATH@|%_builddir|g' %_builddir/config/%{ucprojname}_${file}.file > %_builddir/config/${file}
done

if [ ${ONLINE_TOOL_CONF_ROOT}/configurations/requirements%scram_xml ] ; then 
  cp ${ONLINE_TOOL_CONF_ROOT}/configurations/requirements%scram_xml %_builddir/config/
fi
rm -f %_builddir/config/%{ucprojname}_ignore.file
rm -rf %_builddir/config/site
cp -rf ${ONLINE_TOOL_CONF_ROOT}/configurations/SCRAMToolBox/CMSconfigs %_builddir/config/site
echo $SCRAMV1_VERSION > %_builddir/config/scram_version

pwd
cd %_builddir

echo $PERL5LIB
echo rm -rf %i
mkdir -p $(dirname %i)

%{?buildarch:%buildarch}
export SCRAM_TOOLBOXVERSION=%cmssw_release

mv config/bootsrc config/bootsrc_orig

# Disable building tests, as they bring dependency on cppunit
perl -p -i -e ' s!<ClassPath(.*)test(.*)!!;'  %_builddir/config/BuildFile

# Specify package list for source bootstrap: 
perl -p -e 'if (s/(<download.*)(file:src)(.*)(name="src)(">)/#$1$2$3$4$5/){open $fh, "%_sourcedir/online_build_set" or die; while(readline $fh){chomp;print "$1$2/$_$3$4/$_$5\n"}}' config/bootsrc_orig > config/bootsrc 

%scramcmd project -d $(dirname %i) -b config/bootsrc -f %_builddir/config/site/tools-`cat %_builddir/config/site/sitename`.conf
perl -p -i -e "s|STANDALONE|%v|" %i/.SCRAM/Environment* %i/.SCRAM/%cmsplatf/ToolCache.db
cd %i
%scramcmd setup

%build
pwd
# Remove cmt stuff that brings unwanted dependencies: 
rm -rf `find %{i}/src -type d -name cmt`
echo `%scramcmd arch`
cd %i
cd src

%{?buildarch:%buildarch}

export BUILD_LOG=yes
export SCRAM_NOPLUGINREFRESH=yes
# export SCRAM_NOSYMCHECK=true

if [ $(uname) = Darwin ]; then
  # %scramcmd doesn't know the rpath variable on darwin...
  %scramcmd b echo_null # ensure lib, bin exist
  eval `%scramcmd runtime -sh`
  export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH
fi

%if "%{?nolibchecks:set}" == "set"
export SCRAM_NOLOADCHECK=true
export SCRAM_NOSYMCHECK=true
%endif

%if "%{?preBuildCommand:set}" == "set"
echo "executing %preBuildCommand"
%preBuildCommand
%endif

%if "%{?buildtarget:set}" != "set"
%define buildtarget %{nil} 
%endif

%scramcmd b -r echo_CXX </dev/null
%if "%{?prebuildtarget:set}" == "set"
%scramcmd b --verbose -f %{prebuildtarget} </dev/null
%endif
%scramcmd b --verbose -f %{compileOptions} %{makeprocesses}  %{buildtarget} </dev/null
%if "%{?additionalBuildTarget0:set}" == "set"
%scramcmd b --verbose -f %{additionalBuildTarget0} < /dev/null
%endif
%if "%{?postbuildtarget:set}" == "set"
%scramcmd b --verbose -f %{postbuildtarget} </dev/null
%endif

# strip out dependencies first...
%if "%{?saveDeps:set}" == "set" 
mkdir -p %i/etc/dependencies
chmod +x %{_sourcedir}/findDependencies.pl
%{_sourcedir}/findDependencies.pl -rel %i
gzip %i/etc/dependencies/uses.out
gzip %i/etc/dependencies/usedby.out
%endif


rm -rf %i/tmp
chmod -R 755 %i %i/.SCRAM
(eval `%scramcmd run -sh` ; SealPluginRefresh) || true
rm -fR %i/lib/%cmsplatf/.edmplugincache
(eval `%scramcmd run -sh` ; EdmPluginRefresh) || true

%install
cd %i
%{?buildarch:%buildarch}
perl -p -i -e "s|^#!.*perl(.*)|#!/usr/bin/env perl$1|" $(grep -r -e "^#!.*perl.*" . | cut -d: -f1)
# need writeable directory for profile stuff
mkdir -p etc/scram.d
sed 's|@PROJECT_NAME@|%ucprojname|g;s|@PROJECT_VERSION@|%v|g;s|@PROJECT_BUILD_PATH@|%_builddir|g;s|@PROJECT_ROOT@|%i|g' %_sourcedir/%lcprojname-tool > etc/scram.d/%lcprojname
yes | %scramcmd install # FIXME: do by hand?

%post
cd $RPM_INSTALL_PREFIX/%pkgrel
%{relocateConfig}etc/scram.d/%lcprojname
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $(find config -type f) $(find .SCRAM -type f)
scramver=`cat config/scram_version`
source $RPM_INSTALL_PREFIX/%cmsplatf/lcg/SCRAMV1/$scramver/etc/profile.d/init.sh
%{?buildarch:%buildarch}
yes | %scramcmd install
(rm -rf external/%cmsplatf; ./config/linkexternal.pl --arch %cmsplatf --nolink INCLUDE) || true
eval `%scramcmd run -sh`
for cmd in SealPluginRefresh EdmPluginRefresh IgPluginRefresh ; do
  cmdpath=`which $cmd 2> /dev/null`
  if [ "X$cmdpath" != X ] ; then
    $cmd || true
  fi
done
