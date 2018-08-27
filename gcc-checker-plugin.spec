### RPM external gcc-checker-plugin 1.2
Source0:	https://github.com/cms-externals/CheckerGccPlugins/archive/1.2.tar.gz

BuildRequires: cmake
Requires: gcc

%prep
%setup -n CheckerGccPlugins-1.2

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
