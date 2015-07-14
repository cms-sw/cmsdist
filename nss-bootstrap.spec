### RPM external nss-bootstrap 3.19.2
%define release_version %(echo "%{realversion}" | tr . _)_RTM
Source: https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%{release_version}/src/nss-%{realversion}.tar.gz
Requires: nspr-bootstrap sqlite-bootstrap zlib-bootstrap

%prep
%setup -n nss-%{realversion}

%build
export NSPR_INCLUDE_DIR="${NSPR_BOOTSTRAP_ROOT}/include/nspr"
export NSPR_LIB_DIR="${NSPR_BOOTSTRAP_ROOT}/lib"
export USE_SYSTEM_ZLIB=1
export ZLIB_INCLUDE_DIR="${ZLIB_BOOTSTRAP_ROOT}/include"
export NSS_USE_SYSTEM_SQLITE=1
export SQLITE_INCLUDE_DIR="${SQLITE_BOOTSTRAP_ROOT}/include"
export EXTRA_SHARED_LIBS="-L${ZLIB_BOOTSTRAP_ROOT}/lib -L${SQLITE_BOOTSTRAP_ROOT}/lib"
case %{cmsplatf} in *amd64*|*_mic_*) export USE_64=1 ;; *) ;; esac
make -C ./nss clean
make -C ./nss

%install
case %{cmsplatf} in osx*) soname=dylib ;; *) soname=so ;; esac
install -d %{i}/include/nss3
install -d %{i}/lib
find dist/public/nss -name '*.h' -exec install -m 644 {} %{i}/include/nss3 \;
find . -path "*/dist/*.OBJ/lib/*.${soname}" -exec install -m 755 {} %{i}/lib \;
%define strip_files %{i}/lib
