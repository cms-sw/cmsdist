### RPM external CLUEstering 2.4.0.1
## NOCOMPILER

Source: https://github.com/cms-patatrack/%{n}/archive/%{realversion}.tar.gz
Requires: Alpaka
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
