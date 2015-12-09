### RPM external fastjet-contrib 1.020
%define tag d53aaa4eae502d51154a362d262af2155ed17f38
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&foo=1&output=/%{n}-%{realversion}.tgz
Requires: fastjet
%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
./configure --prefix=%i --fastjet-config=$FASTJET_ROOT/bin/fastjet-config CXXFLAGS="-std=c++11 -I$FASTJET_ROOT/include"

%build
make
make check

%install
make install
make fragile-shared
make fragile-shared-install
