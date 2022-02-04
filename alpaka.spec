### RPM external alpaka develop-20220124
## NOCOMPILER

%define git_commit 26cabb4d5a635c75a75e37d4c4770d3bb71dcd1c

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
