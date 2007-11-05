### RPM external boost 1.33.1-CMS10
# Patches and build fudging by Lassi A. Tuura <lat@iki.fi> (FIXME: contribute to boost)
%define boostver _%(echo %realversion | tr . _)
Source: http://dl.sourceforge.net/sourceforge/%n/%{n}%{boostver}.tar.gz

Requires: boost-build python bz2lib
%if "%{?online_release:set}" != "set"
Requires: zlib
%endif

%prep
%setup -n %{n}%{boostver}

%build
# Note that some targets will fail to build (the test programs have
# missing symbols), causing darwin to fail to link and bjam to return
# an error.  So ignore the exit code from bjam on darwin to avoid
# RPM falsely detecting a problem.
PV="PYTHON_VERSION=$(echo $PYTHON_VERSION | sed 's/\.[0-9]*-.*$//')"
PR="PYTHON_ROOT=$PYTHON_ROOT"

# The following line assumes a version of the form x.y.z-XXXX, where the
# "-XXXX" part represents some CMS rebuild of version x.y.z
BZ2LIBR="BZIP2_LIBPATH=$BZ2LIB_ROOT/lib"
BZ2LIBI="BZIP2_INCLUDE=$BZ2LIB_ROOT/include"

%if "%{?online_release:set}" != "set"
ZLIBR="ZLIB_LIBPATH=$ZLIB_ROOT/lib"
ZLIBI="ZLIB_INCLUDE=$ZLIB_ROOT/include"

case $(uname) in
  Darwin )  bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR -sTOOLS=darwin || true ;;
  * )       bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR -sTOOLS=gcc ;;
esac
%else
bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$BZ2LIBI -sTOOLS=gcc
%endif

%install
boost_abi=$(echo %boostver | sed 's/^_//; s/_0$//')
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
#no debug libs...
#mkdir -p %i/lib/debug
mkdir %i/lib
#(cd bin/boost; find libs -path "libs/*/debug/*.$so" -exec cp {} %i/lib/debug \;)
(cd bin/boost; find libs -path "libs/*/release/*.$so" -exec cp  {} %i/lib/. \;)
find boost -name '*.[hi]*' -print |
  while read f; do
    mkdir -p %i/include/$(dirname $f)
    install -c $f %i/include/$f
  done
find libs -name '*.py' -print |
  while read f; do
    mkdir -p %i/lib/$(dirname $f)
    install -c $f %i/lib/$f
  done
[ $(uname) = Darwin ] &&
  for f in %i/lib/*.$so %i/lib/debug/*.$so; do
    install_name_tool -id $f $f
  done

# Do all manipulation with files before creating symbolic links:
perl -p -i -e "s|^#!.*python|/usr/bin/env python|" $(find %{i}/lib %{i}/bin)
strip %i/lib/*.$so 

(cd %i/lib; for f in lib*-$boost_abi.$so; do ln -s $f $(echo $f | sed "s/-$boost_abi//"); done)
(cd %i/lib; for f in lib*-$boost_abi.$so; do ln -s $f $f.%realversion ; done)
#(cd %i/lib/debug; for f in lib*-d-$boost_abi.$so; do ln -s $f $(echo $f | sed "s/-d-$boost_abi//"); done)
#(cd %i/lib/debug; for f in lib*-d-$boost_abi.$so; do ln -s $f $f.%realversion; done)
(cd %i/lib/libs/python/pyste/install; python setup.py install --prefix=%i)

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# boost toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost version=%v>
<info url="http://www.boost.org"></info>
<lib name=boost_thread-gcc-mt>
<lib name=boost_signals-gcc-mt>
<Client>
 <Environment name=BOOST_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$BOOST_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$BOOST_BASE/include"></Environment>
</Client>
<use name=sockets>
<Runtime name=LD_LIBRARY_PATH value="$BOOST_BASE/lib" type=path>
<Runtime name=CMSSW_FWLITE_INCLUDE_PATH value="$BOOST_BASE/include" type=path>
</Tool>
EOF_TOOLFILE

# boost_filesystem toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_filesystem
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_filesystem version=%v>
<info url="http://www.boost.org"></info>
<lib name=boost_filesystem-gcc-mt>
<use name=boost>
</Tool>
EOF_TOOLFILE

# boost_program_options toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_program_options
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_program_options version=%v>
<info url="http://www.boost.org"></info>
<lib name=boost_program_options-gcc-mt>
<use name=boost>
</Tool>
EOF_TOOLFILE

# boost_python toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_python
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_python version=%v>
<info url="http://www.boost.org"></info>
<lib name=boost_python-gcc-mt>
<Client>
 <Environment name=BOOST_PYTHON_BASE default="%i"></Environment>
 <Environment name=PYSTE_EXEC default="$BOOST_PYTHON_BASE/lib/python2.4/site-packages/Pyste/pyste.py"></Environment>
 <Environment name=LIBDIR default="$BOOST_PYTHON_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$BOOST_PYTHON_BASE/include"></Environment>
</Client>
<use name=elementtree>
<use name=gccxml>
<use name=python>
</Tool>
EOF_TOOLFILE

# boost_regex toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_regex
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_regex version=%v>
<info url="http://www.boost.org"></info>
<lib name=boost_regex-gcc-mt>
<use name=boost>
</Tool>
EOF_TOOLFILE

# boost_signals toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_signals
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_signals version=%v>
<info url="http://www.boost.org"></info>
<lib name=boost_signals-gcc-mt>
<use name=boost>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/boost
%{relocateConfig}etc/scram.d/boost_filesystem
%{relocateConfig}etc/scram.d/boost_program_options
%{relocateConfig}etc/scram.d/boost_python
%{relocateConfig}etc/scram.d/boost_regex
%{relocateConfig}etc/scram.d/boost_signals
