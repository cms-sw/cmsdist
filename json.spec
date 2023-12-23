### RPM external json 3.11.3
## NOCOMPILER

Source: https://github.com/nlohmann/json/archive/refs/tags/v%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DJSON_BuildTests=OFF \
  -DJSON_MultipleHeaders=OFF

make %makeprocesses VERBOSE=1

%install
cd ../build
make install
