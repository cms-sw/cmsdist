### RPM external alpaka develop-20220902
## NOCOMPILER

%define git_commit b518e8c943a816eba06c3e12c0a7e1b58c8faedc

Source: https://github.com/alpaka-group/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
