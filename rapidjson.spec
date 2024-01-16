### RPM external rapidjson 1.1.0
## INCLUDE cpp-standard
Source: https://github.com/Tencent/rapidjson/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: cmake gmake
%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build ; mkdir ../build ; cd ../build
cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DRAPIDJSON_BUILD_TESTS=OFF \
    -DRAPIDJSON_BUILD_DOC=OFF \
    -DRAPIDJSON_BUILD_EXAMPLES=OFF
  
make %{makeprocesses}

%install
cd ../build
make install

