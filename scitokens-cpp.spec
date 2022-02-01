### RPM external scitokens-cpp 0.6.3
Source: https://github.com/scitokens/scitokens-cpp/releases/download/v%{realversion}/%{n}-%{realversion}.tar.gz

BuildRequires: cmake
Requires: libuuid curl sqlite
Patch0: scitokens-cpp

%define soext so
%ifarch darwin
%define soext dylib
%endif

%prep
%setup -n %{n}-%{realversion}

%patch0 -p0

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCURL_INCLUDE_DIR="${CURL_ROOT}/include" \
  -DCURL_LIBRARY="${CURL_ROOT}/lib/libcurl.%{soext}" \
  -DUUID_INCLUDE_DIR="${LIBUUID_ROOT}/include" \
  -DUUID_LIBRARY="${LIBUUID_ROOT}/lib64/libuuid.%{soext}" \
  -DSQLITE3_INCLUDE_DIR="${SQLITE_ROOT}/include" \
  -DSQLITE3_LIBRARY="${SQLITE_ROOT}/lib/libsqlite3.%{soext}"

%install
cd ../build
make %{makeprocesses}
make install
