### RPM external eigen 66e8f38891841bf88ee976a316c0c78a52f0cee5
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## NOCOMPILER
## INCLUDE cpp-standard
%define tag 44c0fd88c1459a9d0e10870a6285a6c7a2943bb5
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
