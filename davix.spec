### RPM external davix 0.8.1

%define tag %(echo R_%{realversion} | tr . _)
%define branch master
%define github_user cern-it-sdc-id
Source0: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define soext so
%ifarch darwin
%define soext dylib
%endif

BuildRequires: cmake gmake
Requires: libxml2 libuuid curl
%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
 -DCMAKE_INSTALL_PREFIX="%{i}" \
 -DEMBEDDED_LIBCURL=FALSE \
 -DDAVIX_TESTS=False \
 -DUUID_LIBRARY="${LIBUUID_ROOT}/lib64/libuuid.%{soext}" \
 -DCMAKE_PREFIX_PATH="${LIBXML2_ROOT};${LIBUUID_ROOT};${CURL_ROOT}"

make VERBOSE=1 %{makeprocesses}

%install
cd ../build
make install

%post
%{relocateConfig}lib64/pkgconfig/davix.pc
