### RPM external boost 1.51.0
%define boostver _%(echo %realversion | tr . _)
Source: http://switch.dl.sourceforge.net/project/%{n}/%{n}/%{v}/%{n}%{boostver}.tar.gz
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

Requires: python bz2lib
%if "%online" != "true"
Requires: zlib
%endif
Patch0: boost-1.47.0-fix-strict-overflow
Patch1: boost-1.47.0-fix-unused
Patch2: boost-1.49.0-explicit_stored_group

%prep
%setup -n %{n}%{boostver}
%patch0 -p1
%patch1 -p1
%patch2 -p1

perl -p -i -e 's/-no-cpp-precomp//' tools/build/v2/tools/darwin.jam \
                                    tools/build/v2/tools/darwin.py
%build
case %cmsos in 
  osx*) TOOLSET=darwin ;;
  *) TOOLSET=gcc ;;
esac

pushd tools/build/v2

sh bootstrap.sh $TOOLSET
popd

PV="PYTHON_VERSION=$(echo $PYTHON_VERSION | sed 's/\.[0-9]*-.*$//')"
PR="PYTHON_ROOT=$PYTHON_ROOT"

# The following line assumes a version of the form x.y.z-XXXX, where the
# "-XXXX" part represents some CMS rebuild of version x.y.z
BZ2LIBR="BZIP2_LIBPATH=$BZ2LIB_ROOT/lib"
BZ2LIBI="BZIP2_INCLUDE=$BZ2LIB_ROOT/include"

if [ ! X%online = "Xtrue" ]
then
  ZLIBR="ZLIB_LIBPATH=$ZLIB_ROOT/lib"
  ZLIBI="ZLIB_INCLUDE=$ZLIB_ROOT/include"
fi

tools/build/v2/bjam %makeprocesses cxxflags="%{cms_cxxflags}" -s$PR -s$PV -s$BZ2LIBR -s$BZ2LIBI ${ZLIBR+-s$ZLIBR} ${ZLIBI+-s$ZLIBI} toolset=$TOOLSET stage

%install
case %cmsos in osx*) so=dylib ;; *) so=so ;; esac
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

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
