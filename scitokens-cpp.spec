### RPM external scitokens-cpp 0.6.3
Source: https://github.com/scitokens/scitokens-cpp/releases/download/v%{realversion}/%{n}-%{realversion}.tar.gz

BuildRequires: cmake
Requires: libuuid curl sqlite
Patch0: scitokens-cpp

%prep
%setup -n %{n}-%{realversion}

%patch0 -p0

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="${CURL_ROOT};${LIBUUID_ROOT};${SQLITE_ROOT}"

%install
cd ../build
make %{makeprocesses}
make install
