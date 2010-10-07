### RPM cms dbs-apps DBS_2_1_5

Requires: dbs-server dbs-client dbs-schema dbs-web

%prep
cd %_builddir
mkdir dbs-apps-dummy
cd dbs-apps-dummy

%build
%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
 echo "source $DBS_SERVER_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_WEB_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $DBS_SERVER_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_CLIENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_WEB_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh

cat > $RPM_INSTALL_PREFIX/setup_dbs.sh << DBS_INIT_EOF
#!/bin/sh
export MYAREA=$RPM_INSTALL_PREFIX
export SCRAM_ARCH=$SCRAM_ARCH
export APT_VERSION=$APT_VERSION
source \$MYAREA/\$SCRAM_ARCH/external/apt/\$APT_VERSION/etc/profile.d/init.sh 
source \$MYAREA/%{pkgrel}/etc/profile.d/init.sh
DBS_INIT_EOF

echo
echo "### To setup environment for this package please use ###"
echo $RPM_INSTALL_PREFIX/setup_dbs.sh

