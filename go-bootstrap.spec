### RPM external go-bootstrap 1.22.6
## NOCOMPILER

Provides: /bin/rc
Source: https://go.dev/dl/go%{realversion}.linux-%{go_package_arch }.tar.gz

%prep
%setup -n go

%build

%install
rsync -a ./ %i/
