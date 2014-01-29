### RPM external dcache-client 1.7.0
#Requires: apache-ant
# Normally requires Ant, but here we use gmake directly 
# in order to avoid dependency on java-jdk.

Provides: libdcap.so
Provides: libpdcap.so

%define downloadv %(echo %v | tr . -)
Source: http://www.dcache.org/downloads/%{v}/dCache-production-%{downloadv}-sources.tar
%prep
%setup -n dCacheBuild/modules/dcap
pwd
chmod a+x `find ./  -type f -name "*.sh"`
%build
make BIN_PATH=%i 
%install
make BIN_PATH=%i install
