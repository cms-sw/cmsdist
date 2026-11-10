### RPM external tinyxml2 11.0.0
%define keep_archives true
Source: https://github.com/leethomason/%{n}/archive/%{realversion}.tar.gz

BuildRequires: gmake cmake

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build ; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DCMAKE_INSTALL_PREFIX="%{i}"

gmake %{makeprocesses} VERBOSE=1

%install
cd ../build
gmake %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib64/pkgconfig/tinyxml2.pc
