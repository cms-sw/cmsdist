### RPM external go 1.13.8
## NOCOMPILER

%ifarch x86_64                                                                                                                                                                                        
Source: https://storage.googleapis.com/golang/go%{realversion}.linux-amd64.tar.gz
%endif
%ifarch ppc64le
Provides: libc.so.6(GLIBC_2.2.5)(64bit)
Source: https://storage.googleapis.com/golang/go%{realversion}.linux-ppc64le.tar.gz
%endif
%ifarch aarch64
Source: https://storage.googleapis.com/golang/go%{realversion}.linux-arm64.tar.gz
%endif

Provides: /bin/rc

%prep
%setup -n go

%build

%install
rsync -a ./ %i/
