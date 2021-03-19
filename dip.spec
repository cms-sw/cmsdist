### RPM external dip 8693f00cc422b4a15858fcd84249acaeb07b6316
%define keep_archives true
Source0: git+https://:@gitlab.cern.ch:8443/industrial-controls/services/dip-hq/dip.git?obj=develop/%{realversion}&export=%{n}&output=/%{n}-%{realversion}.tgz

%define xtag f41e221f8fb95830fc001dad975b4db770f5d29d
Source1: git+https://:@gitlab.cern.ch:8443/industrial-controls/services/dip-hq/platform-dependent.git?obj=develop/%{xtag}&export=platform-dependent&output=/platform-dependent-%{xtag}.tgz
BuildRequires: cmake ninja py3-conan

%prep
%setup -D -T -b 0 -n dip
sed -i -e '/^\s*cmake.test()/d' conanfile.py
%setup -D -T -b 1 -n platform-dependent

%build
rm -rf %{_builddir}/build && mkdir %{_builddir}/build
export CONAN_USER_HOME=%{_builddir}/build
cd %{_builddir}/platform-dependent
conan create .

cd %{_builddir}/dip
conan create . --build=dip --build=log4cplus

%install
mv %{_builddir}/build/.conan/data/dip/*/_/_/package/*/include %{i}/include
mv %{_builddir}/build/.conan/data/dip/*/_/_/package/*/lib     %{i}/lib
mv %{_builddir}/build/.conan/data/log4cplus/*/_/_/package/*/include/log4cplus %{i}/include/log4cplus
mv %{_builddir}/build/.conan/data/log4cplus/*/_/_/package/*/lib/* %{i}/lib/
