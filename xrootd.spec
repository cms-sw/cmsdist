### RPM external xrootd 5.7.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define strip_files %i/lib
%define tag %{realversion}
%define branch master
%define github_user xrootd
Source: https://github.com/xrootd/xrootd/releases/download/v%{realversion}/%{n}-%{realversion}.tar.gz

BuildRequires: cmake gmake autotools py3-pip
Requires: zlib libuuid curl davix
Requires: python3 py3-setuptools
Requires: libxml2

Requires: isal

%define soext so
%ifarch darwin
%define soext dylib
%endif

%prep
%setup -n %{n}-%{realversion}
sed -i -e 's|^ *check_library_exists("uuid" "uuid_generate_random".*$|set(_have_libuuid True)|' cmake/Findlibuuid.cmake

%build
# By default xrootd has fuse, krb5, readline, and crypto enabled.
# libfuse is not produced by CMSDIST.

rm -rf ../build; mkdir ../build; cd ../build
cmake ../%n-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DFORCE_ENABLED=ON \
  -DENABLE_FUSE=FALSE \
  -DENABLE_VOMS=FALSE \
  -DXRDCL_ONLY=TRUE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DENABLE_PYTHON=TRUE \
  -DENABLE_HTTP=TRUE \
  -DENABLE_XRDEC=TRUE \
  -DXRD_PYTHON_REQ_VERSION=3 \
  -DPIP_OPTIONS="--verbose" \
  -DCMAKE_CXX_FLAGS="-I${LIBUUID_ROOT}/include" \
  -DCMAKE_SHARED_LINKER_FLAGS="-L${LIBUUID_ROOT}/lib64" \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

make %makeprocesses VERBOSE=1

%install
cd ../build
make install
%{relocatePy3SitePackages}

%post
%{relocateConfig}bin/xrootd-config
%{relocateConfig}lib64/cmake/XRootD/XRootDConfig.cmake
