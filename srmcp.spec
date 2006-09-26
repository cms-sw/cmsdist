### RPM external srmcp 1.23
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
if [ ! -f $HOME/.srmconfig/config.xml ]; then
  mkdir -p %i/etc $HOME/.srmconfig
  SRM_PATH=%i/srmclient %i/srmclient/sbin/srm \
    -copy file:////dev/null file:////dev/null > /dev/null 2>&1 || true
  [ -f $HOME/.srmconfig/config.xml ] 
fi

mkdir -p %i/etc
cp -p $HOME/.srmconfig/config.xml %i/etc/config.xml
perl -p -i -e "s|$HOME|%i|" %i/etc/config.xml

%post
%{relocateConfig}etc/config.xml
