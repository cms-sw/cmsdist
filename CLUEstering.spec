### RPM external CLUEstering 2.7.0
## NOCOMPILER

Source: https://gitlab.cern.ch/kalos/%{n}/-/archive/%{realversion}/%{n}-%{realversion}.tar.gz
Requires: alpaka
Requires: boost

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -ar include %{i}/include
