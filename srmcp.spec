### RPM external srmcp 1.24
## INITENV +PATH PATH %i/srmclient/bin
## INITENV SET SRM_PATH %i/srmclient
## INITENV SET SRM_CONFIG %i/etc/config.xml

%define downloadv %(echo %v | tr . _)
Source: https://srm.fnal.gov/twiki/pub/SrmProject/SrmcpClient/%{n}_v%{downloadv}_NULL.tar

%prep
%setup -n srmclient
%build

%install
unset SRM_PATH SRM_CONFIG || true
(cd .. && tar -cf - srmclient) | (cd %i && tar -xf -)
mkdir -p %i/etc
SRM_PATH=%i/srmclient SRM_CONFIG=%i/etc/config.xml \
  %i/srmclient/sbin/srm \
    -x509_user_trusted_certificates /etc/grid-security/certificates \
    -copy file:////dev/null file:////dev/null > /dev/null 2>&1 || true

perl -p -i -e "s|$HOME|%i|" %i/etc/config.xml

%post
%{relocateConfig}etc/config.xml
