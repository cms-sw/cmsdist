### RPM external alpaka 1.1.0
## NOCOMPILER

%define git_commit 1.1.0

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
