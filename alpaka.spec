### RPM external alpaka develop-20230621
## NOCOMPILER

%define git_commit 8d4b8df9f1d0477e685e8d1581326b65707f404d

Source: https://github.com/cms-patatrack/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
