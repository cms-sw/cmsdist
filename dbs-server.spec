### RPM cms dbs-server DBS_2_1_6

%define cvstag %{realversion}
# define version of DBS to use, it's schema version
%define dbs_version %{realversion}

Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: apache-ant mysql mysql-deployment oracle apache-tomcat java-jdk dbs-schema dbs-libs

%prep
%setup -n DBS

%build
# DBS wants to have LibValut attached to DBS top-level dir, required by build.xml file
ln -s $DBS_LIBS_ROOT/lib LibValut
echo "PWD=$PWD"
cd Servers/JavaServer

# compile DBS server code
mkdir -p bin/WEB-INF/lib
echo "PWD=$PWD"
source $JAVA_JDK_ROOT/etc/profile.d/init.sh
export JAVA_HOME=$JAVA_JDK_ROOT 
ant --noconfig dist
cd ../../

%install
mkdir -p %{i}/Servers/JavaServer/bin/WEB-INF/lib
cp -r Servers/JavaServer/* %{i}/Servers/JavaServer
ln -s $DBS_LIBS_ROOT/lib %{i}/LibValut

mkdir -p %{i}/etc/profile.d
(echo "#!/bin/sh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_DEPLOYMENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $APACHE_TOMCAT_ROOT/etc/profile.d/init.sh"; \
 echo "source $APACHE_ANT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_LIBS_ROOT/etc/profile.d/init.sh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.sh"; \
 echo "export JAVA_HOME=$JAVA_JDK_ROOT"
 echo "export CATALINA_HOME=$APACHE_TOMCAT_ROOT"
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_DEPLOYMENT_ROOT/etc/profile.d/init.csh"; \
 echo "source $APACHE_TOMCAT_ROOT/etc/profile.d/init.csh"; \
 echo "source $APACHE_ANT_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.csh"; \
 echo "source $DBS_LIBS_ROOT/etc/profile.d/init.csh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.csh"; \
 echo "setenv JAVA_HOME $JAVA_JDK_ROOT"
 echo "setenv CATALINA_HOME $APACHE_TOMCAT_ROOT"
 ) > %{i}/etc/profile.d/dependencies-setup.csh

 
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# Fix path in dbs_init.sh file since now we know install area
cat $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh | \
    sed "s,scram_arch,$SCRAM_ARCH,g" | \
    sed "s,apt_version,$APT_VERSION,g" | \
    sed "s,rpm_install_area,$RPM_INSTALL_PREFIX,g" > \
    $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh.new
/bin/mv -f $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh.new $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh
echo "+++ Fix path in dbs_init.sh"
chmod a+x $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh

# made correct link to LibValut
rm -f $DBS_SERVER_ROOT/LibValut
ln -s $DBS_LIBS_ROOT/lib $DBS_SERVER_ROOT/LibValut

