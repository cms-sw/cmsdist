### RPM external eigen 3.3.0
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## NOCOMPILER
%define tag 70dcc5877552891d260d6e212cb81f36553c9514
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/eigen.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake

%prep
%setup -n %n-%{realversion}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} ../

%install
cd build
make install

%post
%{relocateConfig}share/pkgconfig/eigen3.pc
