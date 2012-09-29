### RPM external boost 1.44.0
%define boostver _%(echo %realversion | tr . _)
Source: http://switch.dl.sourceforge.net/project/%{n}/%{n}/%{v}/%{n}%{boostver}.tar.gz
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
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
