### RPM external xtd c11bc33007a0ae3d7ea692090d695df1f3b93b27
## NOCOMPILER

%define git_commit %{realversion}

Source: https://github.com/cms-patatrack/%{n}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar LICENSE      %{i}/LICENSE
cp -ar README.md    %{i}/README.md
cp -ar include      %{i}/include

%post
