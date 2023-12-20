### RPM external alpaka develop-20230621
## NOCOMPILER

%define git_commit 0286cd8fa24e50179e24b62a48c89201e51eb80a

Source: https://github.com/cms-patatrack/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
