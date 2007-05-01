### RPM external dcap 1.2.35
# Fakes the presence of dcap since we are not allowed to distribute it.
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%v.tar.gz
Patch: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%v.patch
%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif

Provides: libdcap.so%{libsuffix}
Provides: libpdcap.so%{libsuffix}
%prep
%setup -n %n-%v
%patch0 -p1
%build
make BIN_PATH=%i %makeprocesses 
%install
make BIN_PATH=%i install
#
