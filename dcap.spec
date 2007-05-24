### RPM external dcap 1.2.35-XXXX
# Fakes the presence of dcap since we are not allowed to distribute it.
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%realversion.tar.gz
Patch: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%realversion.patch
%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif

Provides: libdcap.so%{libsuffix}
Provides: libpdcap.so%{libsuffix}
%prep
rm -rf %n-%realversion
%setup -n %n-%realversion
%patch0 -p1
%build
rm -rf %i
mkdir -p %i
LD=gcc make BIN_PATH=%i %makeprocesses 
%install
LD=gcc make BIN_PATH=%i install
