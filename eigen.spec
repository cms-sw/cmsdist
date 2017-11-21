### RPM external eigen c7dc0a897676
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
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DBUILD_TESTING=OFF ../

%install
cd build
make install

%post
%{relocateConfig}share/pkgconfig/eigen3.pc
