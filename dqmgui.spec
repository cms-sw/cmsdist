### RPM cms dqmgui 7.4.3.1
## INITENV +PATH PATH %i/xbin
## INITENV +PATH %{dynamic_path_var} %i/xlib
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH $ROOT_ROOT/lib

%define webdoc_files %{installroot}/%{pkgrel}/doc
%define cvs cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define flavors '' 128 

Source0: git+https://github.com/rovere/dqmgui.git?obj=master/6.6.1&export=Monitoring&output=/Monitoring.tar.gz
#Source0: git+:///build1/rovere/GUIDevelopment/GHM?obj=RovereDevelopment&export=Monitoring&output=/Monitoring.tar.gz
#Source0: %{svn}?scheme=svn+ssh&strategy=export&module=Monitoring&output=/src.tar.gz
# For documentation, please refer to http://cms-sw.github.io/pkgtools/fetching-sources.html
Source1: git+https://github.com/cms-sw/cmssw.git?obj=CMSSW_7_0_X/CMSSW_7_0_0_pre1&export=./&filter=*DQMServices/Core*&output=/DQMCore.tar.gz
#Source1: %{cvs}&strategy=export&module=CMSSW/DQMServices/Core&export=DQMServices/Core&tag=-rV03-15-19&output=/DQMCore.tar.gz
Source2: svn://rotoglup-scratchpad.googlecode.com/svn/trunk/rtgu/image?module=image&revision=10&scheme=http&output=/rtgu.tar.gz
Source3: http://opensource.adobe.com/wiki/download/attachments/3866769/numeric.tar.gz
Source4: git+https://github.com/rovere/dqmgui.git?obj=index128/7.4.3&export=Monitoring&output=/Monitoring128.tar.gz
#Source4: git+:///build1/rovere/GUIDevelopment/GHM?obj=Develop128&export=Monitoring&output=/Monitoring128.tar.gz
Patch0: dqmgui-rtgu

Requires: cherrypy py2-cheetah yui extjs gmake pcre boost root libpng libjpg classlib rotatelogs py2-pycurl py2-cjson libuuid d3 protobuf
BuildRequires: py2-sphinx

%prep
# Unpack sources.
%setup -c    -T -a 1 -n stuff
%setup -c -D -T -a 2 -n stuff/rtgu
%patch0 -p1
%setup -c -D -T -a 3 -n stuff/boost/gil/extension
perl -p -i -e '/#include/ && s|\.\./\.\./|boost/gil/|' $(find . -name *.hpp)
chmod 644 $(find . -name *.hpp)

# Legacy Server
%setup -T -b 0 -n Monitoring
# Updated to 128bits-key Server
%setup -c -T -a 4 -n Monitoring128
mv Monitoring/* .
rm -fr Monitoring/

for flavor in %{flavors}; do
  cd ../Monitoring$flavor
  perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/*/conf.py

  # Adapt CMSSW sources to our build.
  cp -pr %_builddir/stuff/{rtgu,boost} src/cpp
  for f in DQM{Store,Error,Net}.{h,cc} MonitorElement.{h,cc} \
           Q{Test,Report,StatisticalTests}.{h,cc} \
           Standalone.h DQM{Channel,Definitions}.h \
           DQMCollector.cpp; do
    dest=src/cpp/DQM/$(basename $f | sed 's/\.cpp/.cc/')
    cp %_builddir/stuff/DQMServices/Core/*/$f $dest
    perl -p -i -e 's{DQMServices/Core/(interface|src)/}{DQM/}g' $dest
    case $f in Standalone.h )
      perl -p -i -e 's|(?=std::string getReleaseVersion)|inline |' $dest ;;
    esac
    chmod 644 $dest
  done
  # Generate makefile fragment for externals.
  case $flavor in
    '' )
      libs=". %i/xlib %i/lib"
      incs=". %i/xinclude %i/include"
      ;;
    * )
      libs=". %i/$flavor/xlib %i/$flavor/lib"
      incs=". %i/$flavor/xinclude %i/$flavor/include"
      ;;
  esac
  dirs="$CLASSLIB_ROOT $BOOST_ROOT $PYTHON_ROOT $ROOT_ROOT
        $ZLIB_ROOT $PCRE_ROOT $LIBPNG_ROOT $LIBJPG_ROOT $PROTOBUF_ROOT"
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

done

# Build
%build
for flavor in %{flavors}; do
  cd ../Monitoring$flavor
  python setup.py -v build_system -s DQM
done

# Install
%install
for flavor in %{flavors}; do
  cd ../Monitoring$flavor
  case $flavor in
    '' )
      mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,include,data} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
      ;;
    * )
      mkdir -p %i/$flavor/etc/profile.d %i/$flavor/{x,}{bin,lib,include,data} %i/$flavor/{x,}$PYTHON_LIB_SITE_PACKAGES
      ;;
  esac
  python setup.py install_system -s DQM --prefix=%i/$flavor
  find %i/$flavor -name '*.egg-info' -exec rm {} \;

  # Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
  : > %i/$flavor/etc/profile.d/dependencies-setup.sh
  : > %i/$flavor/etc/profile.d/dependencies-setup.csh
  for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
    root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
    if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
      echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/$flavor/etc/profile.d/dependencies-setup.sh
      echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/$flavor/etc/profile.d/dependencies-setup.csh
    fi
  done

  # Generate an env.sh which sets a few things more than init.sh.
  (echo ". %i/etc/profile.d/init.sh;"
   echo "export YUI_ROOT EXTJS_ROOT D3_ROOT;"
   echo "export DQMGUI_VERSION='%{realversion}';" # for visDQMUpload
   echo "export MONITOR_ROOT='%i';") > %i/$flavor/etc/profile.d/env.sh
done

%post
for flavor in %{flavors}; do
 %{relocateConfig}/$flavor/etc/makefile.ext
 %{relocateConfig}/etc/profile.d/{env,dep*}.*sh
  case $flavor in
    '' )
      ;;
    * )
      # Do a manual copy and relocation here, since the central
      # one will skip the $flavor at the end of the RPM_INTALL_PREFIX.
      # The main relocation already took place (order of '' and other
      # flavor matter!): here we simply need to append the flavor.
      cp $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.*sh $RPM_INSTALL_PREFIX/%{pkgrel}/$flavor/etc/profile.d
      %{relocateConfig}/$flavor/etc/profile.d/{env,dep*}.*sh
      perl -p -i -e "s|\\Q%{pkgrel}\\E|%{pkgrel}/$flavor|g" $RPM_INSTALL_PREFIX/%{pkgrel}/$flavor/etc/profile.d/env.*sh
      perl -p -i -e "s|\\Q%{pkgrel}\\E|%{pkgrel}/$flavor|g" $RPM_INSTALL_PREFIX/%{pkgrel}/$flavor/etc/profile.d/init.*sh
      ;;
    esac
done

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
