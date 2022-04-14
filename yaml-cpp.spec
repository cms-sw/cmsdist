### RPM external yaml-cpp 0.7.0
Source: https://github.com/jbeder/yaml-cpp/archive/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

%prep
%setup -n %{n}-%{n}-%{realversion}

%build
cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DYAML_CPP_BUILD_TESTS=OFF \
  -DBUILD_SHARED_LIBS=YES

make %{makeprocesses} VERBOSE=1

%install
make install

%post
