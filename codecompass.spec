### RPM external codecompass 1.0
%define github_user cms-externals
Source: https://github.com/%{github_user}/CodeCompass/archive/%{realversion}.tar.gz

BuildRequires: cmake
Requires: thrift odb python sqlite graphviz git java-env boost llvm

%prep
%setup -n CodeCompass-%{realversion}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DDATABASE=sqlite -DCMAKE_BUILD_TYPE=RelWithDebug ../CodeCompass-%{realversion}

%install
cd build
make install
