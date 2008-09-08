### RPM cms dbs-apps 2_0_2

#Requires: dbs-server dbs-client dbs-schema dbs-light dbs-web
Requires: dbs-server dbs-client dbs-schema dbs-web
Source: none

%prep
cd %_builddir
mkdir dbs-apps-dummy
cd dbs-apps-dummy
cp -f %_sourcedir/none .
%build
%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
 echo "source $DBS_SERVER_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_LIGHT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_WEB_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $DBS_SERVER_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_LIGHT_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_WEB_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
