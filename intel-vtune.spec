## INCLUDE oneapi-config
### RPM external intel-vtune %{oneapi_version}
## NOCOMPILER
## INITENV SET INTEL_VTUNE_INSTALLDIR ${CERN_ONEAPI_ROOT}/vtune
Requires: cern-oneapi
Source: none

%prep
%build
%install
