### RPM external xtd fdcc02011bbb1941f6b2c1226a9983a77d5a056e
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
