### RPM external scitokens-cpp 0.7.0
Source: https://github.com/scitokens/%{n}/archive/refs/tags/v%{realversion}.tar.gz

BuildRequires: cmake gmake
Requires: libuuid curl sqlite openssl
Patch0: scitokens-cpp

%prep
%setup -n %{n}-%{realversion}
%patch0 -p0
sed -i -e 's/ -Werror//' CMakeLists.txt

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DOPENSSL_ROOT_DIR:PATH=${OPENSSL_ROOT} \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_PREFIX_PATH="${CURL_ROOT};${LIBUUID_ROOT};${SQLITE_ROOT}"

%install
cd ../build
make %{makeprocesses}
make install
