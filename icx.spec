## INCLUDE oneapi-config
### RPM external icx %{oneapi_version}
## NOCOMPILER
%define skip_license_checks 1
Requires: cern-oneapi
Source: none
Provides: libimf.so()(64bit)
Provides: libintlc.so.5()(64bit)
Provides: libirng.so()(64bit)
Provides: libsvml.so()(64bit)

%prep
%build
%install
ln -sf ../../cern-oneapi/${CERN_ONEAPI_VERSION}/compiler "%{i}/installation"
