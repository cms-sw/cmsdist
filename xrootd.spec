### RPM external xrootd 4.12.3
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define tag b122d662f80a46a570876afd32cdaa9f4370dc1d
%define branch stable-4.12.x
%define github_user xrootd
Source: git+https://github.com/%github_user/xrootd.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake autotools
Requires: zlib
Requires: python3
Requires: libxml2

%define soext so
%ifarch darwin
%define soext dylib
%endif

%prep
%setup -n %n-%{realversion}

%build
# By default xrootd has perl, fuse, krb5, readline, and crypto enabled. 
# libfuse and libperl are not produced by CMSDIST.

rm -rf build; mkdir build; cd build
cmake .. \
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
  -DCMAKE_CXX_FLAGS="-I${LIBUUID_ROOT}/include" \
  -DUUID_INCLUDE_DIR="${LIBUUID_ROOT}/include" \
  -DUUID_LIBRARY="${LIBUUID_ROOT}/lib64/libuuid.%{soext}" \
  -DCMAKE_PREFIX_PATH="${PYTHON3_ROOT};${LIBXML2_ROOT};${LIBUUID_ROOT}"

make %makeprocesses VERBOSE=1
make install
%{relocatePy3SitePackages}

%install
%define strip_files %i/lib
