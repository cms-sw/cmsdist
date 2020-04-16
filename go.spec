### RPM external go 1.13.8

Source: https://storage.googleapis.com/golang/go%{realversion}.linux-amd64.tar.gz

Provides: /bin/rc

%prep
%setup -n go

%build

%install
cp -r * %i
