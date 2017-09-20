### RPM external eigen f3a22f35b044
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## NOCOMPILER
%define tag %{realversion}
Source: https://bitbucket.org/%{n}/%{n}/get/%{tag}.tar.gz
BuildRequires: cmake

%prep
%setup -n %n-%n-%{realversion}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} ../

%install
cd build
make install

%post
%{relocateConfig}share/pkgconfig/eigen3.pc
