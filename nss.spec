### RPM external nss 3.12.9
Source: https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%(echo %realversion | tr . _)_RTM/src/nss-%realversion.tar.gz
Requires: nspr zlib sqlite
Patch0: nss-3.12.6-remove-appleisms
Patch1: nss-3.12.9-add-ZLIB-LIBS-DIR
Patch2: nss-3.12.9-add-SQLITE-LIBS-DIR

%prep
%setup -n nss-%realversion
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
export NSPR_INCLUDE_DIR=$NSPR_ROOT/include/nspr 
export NSPR_LIB_DIR=$NSPR_ROOT/lib
export USE_SYSTEM_ZLIB=1
export ZLIB_LIBS_DIR="-L$ZLIB_ROOT/lib"
export NSS_USE_SYSTEM_SQLITE=1
export SQLITE_INCLUDE_DIR="$SQLITE_ROOT/include"
export SQLITE_LIBS_DIR="-L$SQLITE_ROOT/lib"
export USE_64=1

make -C ./mozilla/security/coreconf clean
make -C ./mozilla/security/dbm clean
make -C ./mozilla/security/nss clean
make -C ./mozilla/security/coreconf
make -C ./mozilla/security/dbm
make -C ./mozilla/security/nss

%install
case %cmsplatf in
  osx*)
    soname=dylib ;;
  *)
    soname=so ;;
esac
rm -rf %i/lib/libsoftokn3*
rm -rf %i/lib/libsql*

install -d %i/include/nss3
install -d %i/lib
find mozilla/dist/public/nss -name '*.h' -exec install -m 644 {} %i/include/nss3 \;
find . -path "*/mozilla/dist/*.OBJ/lib/*.$soname" -exec install -m 755 {} %i/lib \;
%define strip_files %i/lib
