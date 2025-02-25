### RPM external CLUEstering 2.6.2
## NOCOMPILER

Source: https://gitlab.cern.ch/kalos/%{n}/archive/${realversion}/%{n}-${realversion}.tar.gz
Requires: Alpaka
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
