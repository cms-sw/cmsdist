### RPM external alpaka 0.4.0
## NOCOMPILER

Source: https://github.com/alpaka-group/%{n}/archive/%{realversion}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{realversion}

%build

%install
cp -ar include %{i}/include

%post
