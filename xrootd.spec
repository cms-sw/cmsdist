### RPM external xrootd 5.4.2
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define strip_files %i/lib
%define tag 332967cdc6553aebff0fd356254d4cdab9c9e515
%define branch master
%define github_user xrootd
Source: git+https://github.com/%github_user/xrootd.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch: xrootd-ssl3
BuildRequires: cmake gmake autotools
Requires: zlib libuuid
Requires: python3
Requires: libxml2
Requires: scitokens-cpp

%define soext so
%ifarch darwin
%define soext dylib
%endif

%prep
%setup -n %n-%{realversion}
%patch -p1
sed -i -e 's|UUID REQUIRED|UUID |' cmake/XRootDFindLibs.cmake

%build
# By default xrootd has perl, fuse, krb5, readline, and crypto enabled. 
# libfuse and libperl are not produced by CMSDIST.

rm -rf ../build; mkdir ../build; cd ../build
cmake ../%n-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=FALSE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DENABLE_PYTHON=TRUE \
  -DXRD_PYTHON_REQ_VERSION=3 \
  -DWITH_OPENSSL3=TRUE \
  -DCMAKE_CXX_FLAGS="-I${LIBUUID_ROOT}/include" \
  -DUUID_INCLUDE_DIR="${LIBUUID_ROOT}/include" \
  -DUUID_LIBRARY="${LIBUUID_ROOT}/lib64/libuuid.%{soext}" \
  -DSCITOKENS_CPP_DIR="${SCITOKENS_CPP_ROOT}" \
  -DCMAKE_PREFIX_PATH="${PYTHON3_ROOT};${LIBXML2_ROOT};${LIBUUID_ROOT};${SCITOKENS_CPP_ROOT}"


make %makeprocesses VERBOSE=1

%install
cd ../build
make install
%{relocatePy3SitePackages}
