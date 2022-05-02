### RPM external alpaka develop-20220427
## NOCOMPILER

%define git_commit 879b95ffce2da499c9cc6e12d4cfd5545effa701

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
