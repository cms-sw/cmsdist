### RPM external fastjet-contrib 1.033
%define tag 69e835bfc3d36adfe70a1355a2773bc05d9f5599
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
# bla bla
