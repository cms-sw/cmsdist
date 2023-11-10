### RPM external yaml-cpp 0.8.0

Source: https://github.com/jbeder/yaml-cpp/archive/refs/tags/%{realversion}.tar.gz

BuildRequires: cmake ninja

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
  -DYAML_BUILD_SHARED_LIBS=ON \
  -DYAML_CPP_BUILD_TESTS=OFF

ninja -v %{makeprocesses}

%install
cd ../build
ninja %{makeprocesses} install

%post
%{relocateConfig}lib64/pkgconfig/yaml-cpp.pc
