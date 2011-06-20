### RPM external boost 1.42.0
%define boostver _%(echo %realversion | tr . _)
Source: http://internap.dl.sourceforge.net/sourceforge/%{n}/%{n}%{boostver}.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Requires: boost-build python bz2lib
%if "%online" != "true"
Requires: zlib
%endif

%prep
%setup -n %{n}%{boostver}

%build
PV="PYTHON_VERSION=$(echo $PYTHON_VERSION | sed 's/\.[0-9]*-.*$//')"
PR="PYTHON_ROOT=$PYTHON_ROOT"

# The following line assumes a version of the form x.y.z-XXXX, where the
# "-XXXX" part represents some CMS rebuild of version x.y.z
BZ2LIBR="BZIP2_LIBPATH=$BZ2LIB_ROOT/lib"
BZ2LIBI="BZIP2_INCLUDE=$BZ2LIB_ROOT/include"

%if "%online" != "true"
ZLIBR="ZLIB_LIBPATH=$ZLIB_ROOT/lib"
ZLIBI="ZLIB_INCLUDE=$ZLIB_ROOT/include"

case $(uname) in
  Darwin )  bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR toolset=darwin stage;;
  * )       bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR toolset=gcc stage;;
esac
%else
bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$BZ2LIBI toolset=gcc stage
%endif

%install
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
mkdir -p %i/lib %i/include
# copy files around in their final location.
# We use tar to reduce the number of processes required
# and because we need to build the build hierarchy for
# the files that we are copying.
pushd stage/lib
  find . -name "*.$so*" -type f | tar cf - -T - | (cd %i/lib; tar xfp -)
popd
find boost -name '*.[hi]*' | tar cf - -T - | ( cd %i/include; tar xfp -)

for l in `find %i/lib -name "*.$so.*"`
do
  ln -s `basename $l` `echo $l | sed -e "s|[.]$so[.].*|.$so|"`
done

pushd libs/python/pyste/install
  python setup.py install --prefix=%i
popd

# Do all manipulation with files before creating symbolic links:
perl -p -i -e "s|^#!.*python|/usr/bin/env python|" $(find %{i}/lib %{i}/bin -type f)

getLibName()
{
  libname=`find %i/lib -name "libboost_$1.$so" -exec basename {} \;`
  echo $libname | sed -e 's|[.][^-]*$||;s|^lib||'
}

export BOOST_THREAD_LIB=`getLibName thread`
export BOOST_SIGNALS_LIB=`getLibName signals`
export BOOST_FILESYSTEM_LIB=`getLibName filesystem`
export BOOST_SYSTEM_LIB=`getLibName system`
export BOOST_PROGRAM_OPTIONS_LIB=`getLibName program_options`
export BOOST_PYTHON_LIB=`getLibName python`
export BOOST_REGEX_LIB=`getLibName regex`
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# boost toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.boost.org"/>
    <lib name="@BOOST_THREAD_LIB@"/>
    <lib name="@BOOST_SIGNALS_LIB@"/>
    <client>
      <environment name="BOOST_BASE" default="%i"/>
      <environment name="LIBDIR" default="$BOOST_BASE/lib"/>
      <environment name="INCLUDE" default="$BOOST_BASE/include"/>
    </client>
    <runtime name="LD_LIBRARY_PATH" value="$BOOST_BASE/lib" type="path"/>
    <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$BOOST_BASE/include" type="path"/>
    <use name="sockets"/>
  </tool>
EOF_TOOLFILE

# boost_filesystem toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_filesystem.xml
  <tool name="boost_filesystem" version="%v">
    <info url="http://www.boost.org"/>
    <lib name="@BOOST_FILESYSTEM_LIB@"/>
    <use name="boost_system"/>
    <use name="boost"/>
  </tool>
EOF_TOOLFILE

# boost_system toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_system.xml
  <tool name="boost_system" version="%v">
    <info url="http://www.boost.org"/>
    <lib name="@BOOST_SYSTEM_LIB@"/>
    <use name="boost"/>
  </tool>
EOF_TOOLFILE

# boost_program_options toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_program_options.xml
  <tool name="boost_program_options" version="%v">
    <info url="http://www.boost.org"/>
    <lib name="@BOOST_PROGRAM_OPTIONS_LIB@"/>
    <use name="boost"/>
  </tool>
EOF_TOOLFILE

# boost_python toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_python.xml
  <tool name="boost_python" version="%v">
    <info url="http://www.boost.org"/>
    <lib name="@BOOST_PYTHON_LIB@"/>
    <client>
      <environment name="BOOST_PYTHON_BASE" default="%i"/>
      <environment name="PYSTE_EXEC" default="$BOOST_PYTHON_BASE/lib/python@PYTHONV@/site-packages/Pyste/pyste.py"/>
      <environment name="LIBDIR" default="$BOOST_PYTHON_BASE/lib"/>
      <environment name="INCLUDE" default="$BOOST_PYTHON_BASE/include"/>
    </client>
    <use name="elementtree"/>
    <use name="gccxml"/>
    <use name="python"/>
  </tool>
EOF_TOOLFILE

# boost_regex toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_regex.xml
  <tool name="boost_regex" version="%v">
    <info url="http://www.boost.org"/>
    <lib name="@BOOST_REGEX_LIB@"/>
    <use name="boost"/>
  </tool>
EOF_TOOLFILE

# boost_signals toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_signals.xml
  <tool name="boost_signals" version="%v">
    <info url="http://www.boost.org"/>
    <lib name="@BOOST_SIGNALS_LIB@"/>
    <use name="boost"/>
  </tool>
EOF_TOOLFILE

# boost_header toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_header.xml
  <tool name="boost_header" version="%v">
    <info url="http://www.boost.org"/>
    <client>
      <environment name="BOOSTHEADER_BASE" default="%i"/>
      <environment name="INCLUDE" default="$BOOSTHEADER_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE


perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*

# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $(find $RPM_INSTALL_PREFIX/%pkgrel/etc/scram.d -type f)

# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
