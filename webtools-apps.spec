### RPM cms webtools-apps 10
Requires: sitedb dbs-web jobrobot crabconf sitemon
#Requires: prodrequest sitedb dbs-web fmws webconddb
Source: none

%prep
cd %_builddir
mkdir webtools-apps-dummy
cd webtools-apps-dummy
cp -f %_sourcedir/none .
%build
%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
 echo "source $SITEDB_ROOT/etc/profile.d/init.sh"; \
 echo "source $PRODREQUEST_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_WEB_ROOT/etc/profile.d/init.sh"; \
 echo "source $FMWS_ROOT/etc/profile.d/init.sh"; \
 echo "source $JOBROBOT_ROOT/etc/profile.d/init.sh"; \
 echo "source $CRABCONF_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $SITEDB_ROOT/etc/profile.d/init.csh"; \
 echo "source $PRODREQUEST_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_WEB_ROOT/etc/profile.d/init.csh"; \
 echo "source $FMWS_ROOT/etc/profile.d/init.csh"; \
 echo "source $JOBROBOT_ROOT/etc/profile.d/init.csh"; \
 echo "source $CRABCONF_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
