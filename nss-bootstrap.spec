### RPM external nss-bootstrap 3.19.2
%define release_version %(echo "%{realversion}" | tr . _)_RTM
Source0: https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%{release_version}/src/nss-%{realversion}.tar.gz
# Taken from https://git.fedorahosted.org/cgit/nss-pem.git/ at 429b0222759d8ad8e6dcd29e62875ae3efd69116
Source1: http://davidlt.web.cern.ch/davidlt/vault/nss-pem-20160408.tar.gz
Requires: nspr-bootstrap zlib-bootstrap
Patch0: nss-3.16-0001-Add-support-for-non-standard-location-zlib
Patch1: nss-3.19.2-0002-enable-pem

%define strip_files %{i}/lib

%prep
%setup -T -b0 -n nss-%{realversion}
%setup -T -a1 -D -n nss-%{realversion}
%setup -T -D -n nss-%{realversion}
%patch0 -p1
%patch1 -p1

%build
export NSPR_INCLUDE_DIR="${NSPR_BOOTSTRAP_ROOT}/include/nspr"
export NSPR_LIB_DIR="${NSPR_BOOTSTRAP_ROOT}/lib"
export FREEBL_LOWHASH=1
export FREEBL_NO_DEPEND=1
export BUILD_OPT=1
export NSS_NO_PKCS11_BYPASS=1
export ZLIB_INCLUDE_DIR="${ZLIB_BOOTSTRAP_ROOT}/include"
export ZLIB_LIB_DIR="${ZLIB_BOOTSTRAP_ROOT}/lib"
case "%{cmsplatf}" in
  *_amd64_*|*_aarch64_*|*_ppc64le_*)
    export USE_64=1
    ;;
esac

make -C ./nss/coreconf clean
make -C ./nss/lib/dbm clean
make -C ./nss clean
make -C ./nss/coreconf
make -C ./nss/lib/dbm
make -C ./nss

%install
install -d %{i}/include/nss3
install -d %{i}/lib
find ./dist/public/nss -name '*.h' -exec install -m 644 {} %{i}/include/nss3 \;
find ./dist/*.OBJ/lib \( -name '*.dylib' -o -name '*.so' \) -exec install -m 755 {} %{i}/lib \;
