### RPM external fastjet-contrib 1.014
%define tag f873eacf1e3c46bcf5213db9f86386dc599ab34c
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
