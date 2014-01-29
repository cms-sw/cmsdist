### RPM cms scramv1-wrapper 1.0
Requires: gcc-wrapper
Source: none
Requires: cms-env

%prep
%build
## IMPORT gcc-wrapper
%install
%post
cat << \EOF_BIN_SCRAMV1 > $RPM_INSTALL_PREFIX/bin/scramv1
#!/bin/sh
CMSARCH=`cmsarch`
SCRAM_VERSION=`cat %{instroot}/$CMSARCH/etc/default-scramv1-version`
source %{instroot}/$CMSARCH/lcg/SCRAMV1/$SCRAM_VERSION/etc/profile.d/init.sh
%{instroot}/$CMSARCH/lcg/SCRAMV1/$SCRAM_VERSION/bin/scramv1 $@
EOF_BIN_SCRAMV1
chmod +x $RPM_INSTALL_PREFIX/bin/scramv1
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/bin/scramv1
