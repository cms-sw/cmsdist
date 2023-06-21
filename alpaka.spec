### RPM external alpaka develop-20230621
## NOCOMPILER

%define git_commit 3838fbcd1694b461eb3a3d1b64f2cd24d9cf8bd7

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
