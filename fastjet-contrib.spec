### RPM external fastjet-contrib 1.25
%define tag 40ca24ea2c5ef09162339670fcf96c555928da14
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&foo=1&output=/%{n}-%{realversion}.tgz
Requires: fastjet
%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
./configure --prefix=%{i} --fastjet-config=${FASTJET_ROOT}/bin/fastjet-config CXXFLAGS="-std=c++11 -I${FASTJET_ROOT}/include"

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
