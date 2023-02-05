### RPM external alpaka develop-20230201
## NOCOMPILER

%define git_commit a68c866cc6c3019748cf127b4eac61be38e7f687

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
