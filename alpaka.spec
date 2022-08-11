### RPM external alpaka develop-20220811
## NOCOMPILER

%define git_commit 30d205f46d7f9235dd49b4cccd4d2daaa25e0f04

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
