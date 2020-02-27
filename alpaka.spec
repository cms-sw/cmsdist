### RPM external alpaka 0.4.0
## NOCOMPILER

Source: https://github.com/ComputationalRadiationPhysics/%{n}/archive/%{realversion}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -ar include %{i}/include

%post
