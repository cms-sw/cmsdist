### RPM cms dqmgui 9.3.6
## INITENV +PATH PATH %i/xbin
## INITENV +PATH %{dynamic_path_var} %i/xlib
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH $ROOT_ROOT/lib

%define webdoc_files %{installroot}/%{pkgrel}/128/doc
%define cvs cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e

Source0: git+https://github.com/rovere/dqmgui.git?obj=index128/%realversion&export=Monitoring&output=/Monitoring.tar.gz
#Source0: git+:///build1/rovere/GUIDevelopment/GHM?obj=RovereDevelopment&export=Monitoring&output=/Monitoring.tar.gz
#Source0: %{svn}?scheme=svn+ssh&strategy=export&module=Monitoring&output=/src.tar.gz
# For documentation, please refer to http://cms-sw.github.io/pkgtools/fetching-sources.html
Source1: git+https://github.com/cms-sw/cmssw.git?obj=CMSSW_7_6_X/CMSSW_7_6_0&export=./&filter=*DQMServices*&output=/DQMCore.tar.gz
#Source1: %{cvs}&strategy=export&module=CMSSW/DQMServices/Core&export=DQMServices/Core&tag=-rV03-15-19&output=/DQMCore.tar.gz
Source2: svn://rotoglup-scratchpad.googlecode.com/svn/trunk/rtgu/image?module=image&revision=10&scheme=http&output=/rtgu.tar.gz
Source3: http://opensource.adobe.com/wiki/download/attachments/3866769/numeric.tar.gz
Patch0: dqmgui-rtgu

Requires: python cherrypy py2-cheetah yui extjs gmake pcre boost root rootjs libpng libjpg classlib rotatelogs py2-pycurl py2-cjson libuuid d3 protobuf py2-argparse py2-pytest py2-nose jemalloc
BuildRequires: py2-sphinx

%prep
# Unpack sources.
%setup -c    -T -a 1 -n stuff
%setup -c -D -T -a 2 -n stuff/rtgu
%patch0 -p1
%setup -c -D -T -a 3 -n stuff/boost/gil/extension
perl -p -i -e '/#include/ && s|\.\./\.\./|boost/gil/|' $(find . -name *.hpp)
chmod 644 $(find . -name *.hpp)

%setup -T -b 0 -n Monitoring
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/*/conf.py

# Adapt CMSSW sources to our build.
cp -pr %_builddir/stuff/{rtgu,boost} src/cpp
for f in DQM{Store,Error,Net}.{h,cc} MonitorElement.{h,cc} \
         Q{Test,Report,StatisticalTests}.{h,cc} \
         Standalone.h DQM{Channel,Definitions}.h \
         DQMCollector.cpp ROOTFilePB.proto; do
  dest=src/cpp/DQM/$(basename $f | sed 's/\.cpp/.cc/')
  cp %_builddir/stuff/DQMServices/Core/*/$f $dest
  perl -p -i -e 's{DQMServices/Core/(interface|src)/}{DQM/}g' $dest
  perl -p -i -e 's{#include "FWCore/ServiceRegistry/interface/SystemBounds.h"}{}g' $dest
  case $f in Standalone.h )
    perl -p -i -e 's|(?=std::string getReleaseVersion)|inline |' $dest
    perl -0777 -p -i -e 's|struct SystemBounds {\n(.*?)};|namespace service {\n   struct SystemBounds {\n$1};\n  }|gs' $dest ;;
  esac
  chmod 644 $dest
done
# Generate makefile fragment for externals.
libs=". %i/128/xlib %i/128/lib"
incs=". %i/128/xinclude %i/128/include"
dirs="$CLASSLIB_ROOT $BOOST_ROOT $PYTHON_ROOT $ROOT_ROOT
      $ZLIB_ROOT $PCRE_ROOT $LIBPNG_ROOT $LIBJPG_ROOT $PROTOBUF_ROOT $JEMALLOC_ROOT"
for d in $dirs; do
  libs="$libs $d/lib"
  case $d in
    $PYTHON_ROOT )
      incs="$incs $d/include/python2.7" ;;
    * )
      incs="$incs $d/include" ;;
  esac
done

cat > etc/makefile.ext <<- EOF
 INCLUDE_DIRS = $incs
 LIBRARY_DIRS = $libs
EOF

# Build
%build
python setup.py -v build_system -s DQM -d

# Install
%install
mkdir -p %i/{128,}/etc/profile.d %i/128/{x,}{bin,lib,include,data} %i/128/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s DQM --prefix=%i/128
find %i/128 -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/128/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/128/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate an env.sh which sets a few things more than init.sh.
(echo ". %i/etc/profile.d/init.sh;"
 echo "export YUI_ROOT EXTJS_ROOT D3_ROOT ROOTJS_ROOT;"
 echo "export DQMGUI_VERSION='%{realversion}';" # for visDQMUpload
 echo "export LD_PRELOAD=$JEMALLOC_ROOT/lib/libjemalloc.so.`jemalloc-config --revision`"
 echo "export MONITOR_ROOT='%i';") > %i/128/etc/profile.d/env.sh

%post
%{relocateConfig}/128/etc/makefile.ext
%{relocateConfig}/128/etc/profile.d/{env,dep*}.*sh
cp $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.*sh $RPM_INSTALL_PREFIX/%{pkgrel}/128/etc/profile.d
perl -p -i -e "s|\\Q%{pkgrel}\\E|%{pkgrel}/128|g" $RPM_INSTALL_PREFIX/%{pkgrel}/128/etc/profile.d/env.*sh
perl -p -i -e "s|\\Q%{pkgrel}\\E|%{pkgrel}/128|g" $RPM_INSTALL_PREFIX/%{pkgrel}/128/etc/profile.d/init.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/128/doc

## SUBPACKAGE webdoc
