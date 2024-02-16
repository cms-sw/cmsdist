### RPM external eigen 3bb6a48d8c171cf20b5f8e48bfb4e424fbd4f79e
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## NOCOMPILER
## INCLUDE cpp-standard
%define tag 4dce4ce667e0a8ed2a44f4ee4eafcc3972626f08
%define branch cms/master/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/eigen-git-mirror.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DBUILD_TESTING=OFF -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} ../

%install
cd build
make install

%post
%{relocateConfig}share/pkgconfig/eigen3.pc
