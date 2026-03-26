### RPM external actsdata v10
## NOCOMPILER

%define archive traccc-data-%{realversion}.tar.gz
Source: no-cmssdt-cache+https://acts.web.cern.ch/traccc/data/%{archive}
AutoReqProv: no

# unpack the source archive under ${RPM_INSTALL_PREFIX}/share/package during the
# rpm installation, and create symlinks to ${RPM_INSTALL_PREFIX}/arch/package
%define unpack_at_install 1
## INCLUDE data/shared-data-package
