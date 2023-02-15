### RPM external alpaka develop-20230215
## NOCOMPILER

%define git_commit b849ce43dbfb6d5e1d4279c0025e3b15eddffc32

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
