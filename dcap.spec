### RPM external dcap 1.2.35
# Fakes the presence of dcap since we are not allowed to distribute it.
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%v.tar.gz
Patch: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%v.patch
Provides: libdcap.so
Provides: libpdcap.so
%prep
%setup -n %n-%v
%patch0 -p1
%build
make BIN_PATH=%i %makeprocesses 
%install
make BIN_PATH=%i install
#
