### RPM external alpaka 1.2.0
## NOCOMPILER

%define git_commit 1.2.0

Source: https://github.com/cms-externals/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
