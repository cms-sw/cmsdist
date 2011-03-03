### RPM cms dqmgui 6.0.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages

%define svn svn://svn.cern.ch/reps/CMSDMWM/Monitoring/tags/%{realversion}
%define cvs cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e

Source0: %{svn}?scheme=svn+ssh&strategy=export&module=Monitoring&output=/src.tar.gz
Source1: %{cvs}&strategy=export&module=CMSSW/DQMServices/Core&export=DQMServices/Core&tag=-rV03-15-12&output=/DQMCore.tar.gz
Source2: svn://rotoglup-scratchpad.googlecode.com/svn/trunk/rtgu/image?module=image&revision=10&scheme=http&output=/rtgu.tar.gz
Source3: http://opensource.adobe.com/wiki/download/attachments/3866769/numeric.tar.gz
Patch0: dqmgui-rtgu

Requires: cherrypy py2-cheetah yui extjs gmake pcre boost root libpng libjpg classlib rotatelogs

%prep
# Unpack sources.
%setup -c    -T -a 1 -n stuff
%setup -c -D -T -a 2 -n stuff/rtgu
%patch0 -p1
%setup -c -D -T -a 3 -n stuff/boost/gil/extension
perl -p -i -e '/#include/ && s|\.\./\.\./|boost/gil/|' $(find . -name *.hpp)
%setup -T -b 0 -n Monitoring

# Adapt CMSSW sources to our build.
mv %_builddir/stuff/{rtgu,boost} src/cpp
for f in DQM{Store,Error,Net}.{h,cc} MonitorElement.{h,cc} \
         Q{Test,Report,StatisticalTests}.{h,cc} \
         Standalone.h DQM{Channel,Definitions}.h \
         DQMCollector.cpp; do
  dest=src/cpp/DQM/$(basename $f | sed 's/\.cpp/.cc/')
  mv %_builddir/stuff/DQMServices/Core/*/$f $dest
  perl -p -i -e 's{DQMServices/Core/(interface|src)/}{DQM/}g' $dest
  case $f in Standalone.h )
    perl -p -i -e 's|(?=std::string getReleaseVersion)|inline |' $dest ;;
  esac
  chmod 644 $dest
done

# Generate makefile fragment for externals.
libs=". %i/xlib %i/lib"
incs=". %i/xinclude %i/include"
dirs="$CLASSLIB_ROOT $BOOST_ROOT $PYTHON_ROOT $ROOT_ROOT
      $ZLIB_ROOT $PCRE_ROOT $LIBPNG_ROOT $LIBJPG_ROOT"
for d in $dirs; do
  libs="$libs $d/lib"
  case $d in
    $PYTHON_ROOT )
      incs="$incs $d/include/python2.6" ;;
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
python setup.py -v build_system -s DQM

# Install
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,include,data}
python setup.py install_system -s DQM --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate an env.sh which sets a few things more than init.sh.
(echo ". %i/etc/profile.d/init.sh;"
 echo "export PATH=%i/xbin:\$PATH;"
 echo "export PYTHONPATH=%i/xpython:\$PYTHONPATH;"
 echo "export LD_LIBRARY_PATH=%i/xlib:\$LD_LIBRARY_PATH;"
 echo "export YUI_ROOT='$YUI_ROOT';"
 echo "export EXTJS_ROOT='$EXTJS_ROOT';"
 echo "export DQMGUI_VERSION='$DQMGUI_VERSION';" # for visDQMUpload
 echo "export MONITOR_ROOT='%i';") > %i/etc/profile.d/env.sh

%post
%{relocateConfig}etc/makefile.ext
%{relocateConfig}etc/profile.d/{env,dep*}.*sh
