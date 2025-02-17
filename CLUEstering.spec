### RPM external CLUEstering 2.5.0
## NOCOMPILER

Source: https://github.com/cms-patatrack/%{n}/archive/%{realversion}.tar.gz
Requires: alpaka
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include
