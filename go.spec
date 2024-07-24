### RPM external go 1.22.5
## NOCOMPILER

%ifarch x86_64
%define download_arch amd64
%elifarch aarch64
%define download_arch arm64
%else
%define download_arch   %{_arch}
%endif
Provides: /bin/rc
Source: https://go.dev/dl/go%{realversion}.linux-%{download_arch}.tar.gz

%prep
%setup -n go

%build

%install
rsync -a ./ %i/
