### RPM external eigen 3.2.2
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## NOCOMPILER
%define tag 87b069eefbf748ee3aba16fe5f84b4ccd6227082
%define branch cms/3.2.2
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
