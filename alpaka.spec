### RPM external alpaka 1.1.0
## NOCOMPILER

%define git_commit 1c19cf9e647bbd550148b4b219c0b62255970204

Source: https://github.com/cms-externals/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
