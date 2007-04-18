### RPM external boost 1.33.1
Requires: gcc-wrapper
# Patches and build fudging by Lassi A. Tuura <lat@iki.fi> (FIXME: contribute to boost)
# define boostver -%v <-- for 1.30.2
%define boostver _%(echo %v | tr . _)
Requires: boost-build python bz2lib zlib
Source: http://dl.sourceforge.net/sourceforge/%n/%{n}%{boostver}.tar.gz
#Patch: boost

%prep
%setup -n %{n}%{boostver}
#%patch

%build
## IMPORT gcc-wrapper
# Note that some targets will fail to build (the test programs have
# missing symbols), causing darwin to fail to link and bjam to return
# an error.  So ignore the exit code from bjam on darwin to avoid
# RPM falsely detecting a problem.
PR="PYTHON_ROOT=$PYTHON_ROOT"
PV="PYTHON_VERSION=$(echo $PYTHON_VERSION | sed 's/\.[0-9]*$//')"
BZ2LIBR="BZ2LIB_LIBPATH=$BZ2LIB_ROOT/lib"
ZLIBR="ZLIB_LIBPATH=$ZLIB_ROOT/lib"
BZ2LIBI="BZ2LIB_INCLUDE=$BZ2LIB_ROOT/include"
ZLIBI="ZLIB_INCLUDE=$ZLIB_ROOT/include"

case $(uname) in
  Darwin )  bjam -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR -sTOOLS=darwin || true ;;
  * )       bjam -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR -sTOOLS=gcc ;;
esac

%install
boost_abi=$(echo %boostver | sed 's/^_//; s/_0$//')
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
mkdir -p %i/lib/debug
(cd bin/boost; find libs -path "libs/*/debug/*.$so" -exec cp {} %i/lib/debug \;)
(cd bin/boost; find libs -path "libs/*/release/*.$so" -exec cp {} %i/lib \;)
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

(cd %i/lib; for f in lib*-$boost_abi.$so; do ln -s $f $(echo $f | sed "s/-$boost_abi//"); done)
(cd %i/lib; for f in lib*-$boost_abi.$so; do ln -s $f $f.%v ; done)
(cd %i/lib/debug; for f in lib*-d-$boost_abi.$so; do ln -s $f $(echo $f | sed "s/-d-$boost_abi//"); done)
(cd %i/lib/debug; for f in lib*-d-$boost_abi.$so; do ln -s $f $f.%v; done)
(cd %i/lib/libs/python/pyste/install; python setup.py install --prefix=%i)

perl -p -i -e "s|^#!.*python|/usr/bin/env python|" $(find %{i}/lib %{i}/bin)

#
#
