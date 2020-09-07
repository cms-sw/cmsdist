### RPM external fastjet-contrib 1.044
%define tag 03f2fb3c7e26248f5cab3d6c52fab3e112342113
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&foo=1&output=/%{n}-%{realversion}.tgz
Requires: fastjet
%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
./configure --prefix=%{i} --fastjet-config=${FASTJET_ROOT}/bin/fastjet-config CXXFLAGS="-I${FASTJET_ROOT}/include"

%build
make
make check

%install
make install
make fragile-shared
make fragile-shared-install

# All shared libraries on RH/Fedora are installed with 0755
# RPM requires it to generate requires/provides also (otherwise it ignores the files)
find %{i}/lib -type f | xargs chmod 0755
