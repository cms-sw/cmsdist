### RPM external eigen 82dd3710dac619448f50331c1d6a35da673f764a
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## NOCOMPILER
%define tag 5c78a3657102009ea20604808bf4d5a30df6ec7a
%define branch cms/master/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/eigen-git-mirror.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DBUILD_TESTING=OFF ../

%install
cd build
make install

%post
%{relocateConfig}share/pkgconfig/eigen3.pc
