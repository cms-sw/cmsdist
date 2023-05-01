### RPM external xrootd 5.5.3
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define strip_files %i/lib
%define tag %{realversion}
%define branch master
%define github_user xrootd
Source: git+https://github.com/%github_user/xrootd.git?obj=%{branch}/v%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake gmake autotools
Requires: zlib libuuid curl davix
Requires: python3 py3-setuptools
Requires: libxml2
Requires: scitokens-cpp

%define soext so
%ifarch darwin
%define soext dylib
%endif

%prep
%setup -n %n-%{realversion}
sed -i -e 's|UUID REQUIRED|UUID |' cmake/XRootDFindLibs.cmake

%build
# By default xrootd has perl, fuse, krb5, readline, and crypto enabled. 
# libfuse and libperl are not produced by CMSDIST.

rm -rf ../build; mkdir ../build; cd ../build
cmake ../%n-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DUSER_VERSION=%{realversion} \
  -DCMAKE_BUILD_TYPE=Release \
  -DFORCE_ENABLED=ON \
  -DENABLE_FUSE=FALSE \
  -DENABLE_VOMS=FALSE \
  -DXRDCL_ONLY=TRUE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=TRUE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DENABLE_PYTHON=TRUE \
  -DENABLE_HTTP=TRUE \
  -DXRD_PYTHON_REQ_VERSION=3 \
  -DCMAKE_CXX_FLAGS="-I${LIBUUID_ROOT}/include -I${DAVIX_ROOT}/include" \
  -DUUID_INCLUDE_DIR="${LIBUUID_ROOT}/include" \
  -DUUID_LIBRARY="${LIBUUID_ROOT}/lib64/libuuid.%{soext}" \
  -DSCITOKENS_CPP_DIR="${SCITOKENS_CPP_ROOT}" \
  -DCMAKE_PREFIX_PATH="${ZLIB_ROOT};${PYTHON3_ROOT};${LIBXML2_ROOT};${LIBUUID_ROOT};${SCITOKENS_CPP_ROOT};${CURL_ROOT};${DAVIX_ROOT}"

make %makeprocesses VERBOSE=1

%install
cd ../build
make install
%{relocatePy3SitePackages}

%post
%{relocateConfig}bin/xrootd-config
%{relocateConfig}${PYTHON3_LIB_SITE_PACKAGES}/xrootd-%{realvesion}-*.egg/EGG-INFO/SOURCES.txt
