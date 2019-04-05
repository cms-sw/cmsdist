### RPM external gcc-checker-plugin 1.3

%define tag 7662a4426c22f0878b3cfb5d6b80f1737f57fc4c
Source: git+https://github.com/cms-externals/CheckerGccPlugins.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: cmake
Requires: gcc

%prep
%setup -n %{n}-%{realversion}

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
