### RPM external cub 1.8.0
Source: https://github.com/NVlabs/cub/archive/v%{realversion}.tar.gz
Requires: cuda

%prep
%setup -n %{n}-%{realversion}

%build

%install
mkdir %{i}/include
cp -ar cub %{i}/include/
# bla bla
