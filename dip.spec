### RPM external dip 8693f00cc422b4a15858fcd84249acaeb07b6316
%define keep_archives true
Source0: git+https://:@gitlab.cern.ch:8443/industrial-controls/services/dip-hq/dip.git?obj=develop/%{realversion}&export=%{n}&output=/%{n}-%{realversion}.tgz

%define xtag f41e221f8fb95830fc001dad975b4db770f5d29d
Source1: git+https://:@gitlab.cern.ch:8443/industrial-controls/services/dip-hq/platform-dependent.git?obj=develop/%{xtag}&export=platform-dependent&output=/platform-dependent-%{xtag}.tgz
BuildRequires: cmake gmake
Requires: log4cplus

%prep
%setup -D -T -b 0 -n dip
sed -i -e '/conanbuildinfo.cmake\|conan_basic_setup/d' CMakeLists.txt
sed -i -e 's|CONAN_PKG::||g;s|log4cplus|log4cplusS|' CMakeLists.txt

%setup -D -T -b 1 -n platform-dependent
sed -i -e '/conanbuildinfo.cmake\|conan_basic_setup/d' CMakeLists.txt

%build
cd %{_builddir}; rm -rf build/platform-dependent && mkdir -p build/platform-dependent; cd build/platform-dependent
cmake ../../platform-dependent -DCMAKE_INSTALL_PREFIX=%{i}
gmake %{makeprocesses} VERBOSE=1
gmake install

cd %{_builddir}; rm -rf build/dip && mkdir -p build/dip ; cd build/dip
LDFLAGS="-L${LOG4CPLUS_ROOT}/lib64 -L%{i}/lib" \
  CXXFLAGS="-I%{i}/include -I${LOG4CPLUS_ROOT}/include" \
  cmake ../../dip -DCMAKE_INSTALL_PREFIX=%{i}
gmake %{makeprocesses} VERBOSE=1

%install
cd %{_builddir}/build/dip
gmake install
rm -rf %{i}/lib/cmake
