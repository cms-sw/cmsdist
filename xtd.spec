### RPM external xtd be7dc5807e054ea9a4796c902b5076a7c36ca918
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
