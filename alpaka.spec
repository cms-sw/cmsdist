### RPM external alpaka develop-20220621
## NOCOMPILER

%define git_commit 5a4691c82676176fd8b71e1f57bb809f8c75a095

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
