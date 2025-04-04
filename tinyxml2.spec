### RPM external tinyxml2 6.2.0
Source: https://github.com/leethomason/%{n}/archive/%{realversion}.tar.gz
Source99: modulemaps/tinyxml2_modulemap
BuildRequires: gmake cmake

%prep
%setup -n %setup -q -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build ; cd ../build
cmake ../%{n}-%{realversion} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="%{i}"

gmake %{makeprocesses}

%install
cd ../build
gmake %{makeprocesses} install
cp %{_sourcedir}/tinyxml2_modulemap  %{i}/include/module.modulemap

%post
%{relocateConfig}lib64/pkgconfig/tinyxml2.pc
%{relocateConfig}lib64/cmake/tinyxml2/tinyxml2Targets.cmake
