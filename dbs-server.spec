### RPM cms dbs-server DBS_1_0_8

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: apache-ant mysql mysql-deployment oracle apache-tomcat java-jdk dbs-schema

%prep
%setup -n DBS
# kill running mysql|tomcat under my account since build is over
ps -u`whoami` | grep mysqld | awk '{print "kill -9 "$1""}' |/bin/sh
ps -u`whoami` | grep tomcat | awk '{print "kill -9 "$1""}' |/bin/sh

%build
echo "PWD=$PWD"
cd Servers/JavaServer
# fix context.xml file
cat > etc/context.xml << EOF_CONTEXT
<Context path="/servlet/DBSServlet" docBase="DBSServlet" debug="5" reloadable="true" crossContext="true">
     <SupportedSchemaVersion schemaversion="DBS_1_0_8" />
     <SupportedClientVersions clientversions="DBS_1_0_1, DBS_1_0_5, DBS_1_0_7, DBS_1_0_8, DBS_1_0_9"/>
     <DBSBlockConfig maxBlockSize="2000000000000" maxBlockFiles="100" />
                        
     <Resource name="jdbc/dbs"
              auth="Container"
              type="javax.sql.DataSource"
              maxActive="30"
              maxIdle="10"
              maxWait="10000"
              username="dbs"
              password="cmsdbs"
              driverClassName="org.gjt.mm.mysql.Driver"
              url="jdbc:mysql://localhost:3316/%{cvstag}?autoReconnect=true"/>
</Context>
EOF_CONTEXT

mkdir -p bin/WEB-INF/lib
echo "PWD=$PWD"
source $JAVA_JDK_ROOT/etc/profile.d/init.sh
export JAVA_HOME=$JAVA_JDK_ROOT 
ant --noconfig dist
cd ../../

%install
mkdir -p %{i}/Servers/JavaServer/bin/WEB-INF/lib
cp -r Servers/JavaServer/* %{i}/Servers/JavaServer

# copy war file
cp %{i}/Servers/JavaServer/DBS.war $APACHE_TOMCAT_ROOT/webapps

mkdir -p %{i}/etc/profile.d
(echo "#!/bin/sh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_DEPLOYMENT_ROOT/etc/profile.d/init.sh"; \
 echo "source $APACHE_TOMCAT_ROOT/etc/profile.d/init.sh"; \
 echo "source $APACHE_ANT_ROOT/etc/profile.d/init.sh"; \
 echo "source $DBS_SCHEMA_ROOT/etc/profile.d/init.sh"; \
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
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.csh"; \
 echo "setenv JAVA_HOME $JAVA_JDK_ROOT"
 echo "setenv CATALINA_HOME $APACHE_TOMCAT_ROOT"
 ) > %{i}/etc/profile.d/dependencies-setup.csh

 
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# setup MySQL server
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
VO_CMS_SW_DIR=`echo $DBS_SERVER_ROOT | awk '{split($1,a,SCRAM_ARCH); print a[1]}' SCRAM_ARCH=$SCRAM_ARCH`
export VO_CMS_SW_DIR
$MYSQL_DEPLOYMENT_ROOT/bin/mysql-deployment.sh

# set DBS DBs
MYSQL_PORT=3316
MYSQL_PATH=$MYSQL_ROOT/mysqldb
MYSQL_SOCK=$MYSQL_PATH/mysql.sock
MYSQL_PID=$MYSQL_PATH/mysqld.pid
MYSQL_ERR=$MYSQL_PATH/error.log
# grant permissions to CMS MySQL DBS account
echo "+++ Grand permission to dbs account, DBS DB ${DBS_SCHEMA_VERSION} ..."
echo "$MYSQL_ROOT/bin/mysql -udbs -pcmsdbs --socket=$MYSQL_SOCK"
echo "$DBS_SCHEMA_ROOT/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql"
# DBS uses trigger which requires to have SUPER priveleges, so we'll create DB using root
# and delegate this to dbs account.
$MYSQL_ROOT/bin/mysql -uroot -pcms --socket=$MYSQL_SOCK < $DBS_SCHEMA_ROOT/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql
$MYSQL_ROOT/bin/mysql --socket=$MYSQL_SOCK -uroot -pcms mysql -e "GRANT ALL ON ${DBS_SCHEMA_VERSION}.* TO dbs@localhost;"

# I need to copy/deploy DBS.war file into tomcat area
cp $DBS_SERVER_ROOT/Servers/JavaServer/DBS.war $APACHE_TOMCAT_ROOT/webapps

echo
echo
echo "In order to run DBS server you need to setup the following environment"
echo
echo "#############################################################"
echo "export MYAREA=$RPM_INSTALL_PREFIX"
echo "export SCRAM_ARCH=slc4_ia32_gcc345"
echo "source $MYAREA/slc4_ia32_gcc345/external/apt/0.5.15lorg3.2-CMS3/etc/profile.d/init.sh"
echo "source $DBS_SERVER_ROOT/etc/profile.d/init.sh"
echo "#############################################################"
echo
echo "For your convinience we created setup_dbs.sh file with this settings"
echo "It should be executed each time when you need to start DBS"
echo

# create setup file for users convenience
if [ -e $RPM_INSTALL_PREFIX/setup_dbs.sh ]; then
    echo "+++ Found $RPM_INSTALL_PREFIX/setup_dbs.sh, will keep it as $RPM_INSTALL_PREFIX/setup_dbs.sh.bak"
    /bin/mv -f $RPM_INSTALL_PREFIX/setup_dbs.sh $RPM_INSTALL_PREFIX/setup_dbs.sh.bak
else
    echo "+++ File $RPM_INSTALL_PREFIX/setup_dbs.sh not found, will create"
cat > $RPM_INSTALL_PREFIX/setup_dbs.sh << EOF2
#!/bin/sh
export MYAREA=$RPM_INSTALL_PREFIX
export SCRAM_ARCH=slc4_ia32_gcc345
source $MYAREA/slc4_ia32_gcc345/external/apt/0.5.15lorg3.2-CMS3/etc/profile.d/init.sh 
source $DBS_SERVER_ROOT/etc/profile.d/init.sh
ps -u`whoami` | egrep "mysqld|tomcat" | awk '{print "kill -9 "$1""}' |/bin/sh
echo "+++ Start up CMS MySQL daemon on port ${MYSQL_PORT} ..."
$MYSQL_ROOT/bin/mysqld_safe --datadir=$MYSQL_PATH --port=$MYSQL_PORT \
--socket=$MYSQL_SOCK --log-error=$MYSQL_ERR --pid-file=$MYSQL_PID &
echo "+++ Start tomcat server"
$APACHE_TOMCAT_ROOT/bin/catalina.sh start
EOF2
    chmod a+x $RPM_INSTALL_PREFIX/setup_dbs.sh
fi

# time to start up tomcat for user
$APACHE_TOMCAT_ROOT/bin/catalina.sh start

