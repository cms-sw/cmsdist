### RPM external gcc-checker-plugin 1.3
Source0:	https://github.com/cms-externals/CheckerGccPlugins/archive/%{realversion}.tar.gz

BuildRequires: cmake
Requires: gcc

%prep
%setup -n CheckerGccPlugins-%{realversion}

%build
mkdir build
cd build
cmake ../
make
make test

%install
mkdir lib
cp build/libchecker_gccplugins.so lib
rm -rf build
cp -rp * %{i}
