### RPM cms dbs-server DBS_1_1_2e

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: apache-ant mysql mysql-deployment oracle apache-tomcat java-jdk dbs-schema

%prep
%setup -n DBS
# kill running mysql|tomcat under my account since build is over
ps -w -w -f -u`whoami` | egrep "mysqld|tomcat" | grep -v egrep | awk '{print "kill -9 "$2""}' |/bin/sh

%build
echo "PWD=$PWD"
cd Servers/JavaServer
# fix context.xml file
cat > etc/context.xml << EOF_CONTEXT
<Context path="/servlet/DBSServlet" docBase="DBSServlet" debug="5" reloadable="true" crossContext="true">
     <SupportedSchemaVersion schemaversion="DBS_1_0_9" />
     <SupportedClientVersions clientversions="DBS_1_0_1, DBS_1_0_5, DBS_1_0_7, DBS_1_0_8, DBS_1_0_9, DBS_1_1_2"/>
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

# create dbs init script
mkdir -p %{i}/Servers/JavaServer/bin
cat > %{i}/Servers/JavaServer/bin/dbs_init.sh << DBS_INIT_EOF
#!/bin/sh
export MYAREA=rpm_install_area
export SCRAM_ARCH=slc4_ia32_gcc345
source \$MYAREA/\$SCRAM_ARCH/external/apt/0.5.15lorg3.2-CMS3/etc/profile.d/init.sh 
source \$MYAREA/%{pkgrel}/etc/profile.d/init.sh
# set DBS DBs
MYSQL_PORT=3316
MYSQL_PATH=\$MYSQL_ROOT/mysqldb
MYSQL_SOCK=\$MYSQL_PATH/mysql.sock
MYSQL_PID=\$MYSQL_PATH/mysqld.pid
MYSQL_ERR=\$MYSQL_PATH/error.log

function dbs_stop() 
{
    me=\`whoami\`
    echo $"Stop mysqld|tomcat running under \$me account..."
    ps -w -w -f -u\$me | egrep "mysqld|tomcat" | grep -v egrep | awk '{print "kill -9 "\$2""}'|/bin/sh
}
function dbs_start()
{
    echo "+++ Start up CMS MySQL daemon on port \${MYSQL_PORT} ..."
    \$MYSQL_ROOT/bin/mysqld_safe --datadir=\$MYSQL_PATH --port=\$MYSQL_PORT \
    --socket=\$MYSQL_SOCK --log-error=\$MYSQL_ERR --pid-file=\$MYSQL_PID &
    echo "+++ Start tomcat server"
    \$APACHE_TOMCAT_ROOT/bin/catalina.sh start
    sleep 2
    echo
    echo "DBS service is ready ..."
}
function dbs_status() 
{
    me=\`whoami\`
    dbs_mysqld=\`ps -w -w -f -u\$me | egrep "mysqld" | grep -v egrep | wc -l\`
    dbs_tomcat=\`ps -w -w -f -u\$me | egrep "tomcat" | grep -v egrep | wc -l\`
    if [ \${dbs_tomcat} -ne 1 ]; then
       echo "Tomcat server is not running"
       exit 1
    fi
    if [ \${dbs_mysqld} -ne 2 ]; then
       echo "MySQL server is not running"
       exit 1
    fi
    ps -w -w -f -u\$me | egrep "mysqld" | grep -v egrep | awk '{print "MySQLd server running, pid="\$2""}'
    ps -w -w -f -u\$me | egrep "tomcat" | grep -v egrep | awk '{print "Tomcat server running, pid="\$2""}'
    echo "For more information please have a look at tomcat log:"
    echo "\$APACHE_TOMCAT_ROOT/logs/catalina.out"
}

RETVAL=\$?

case "\$1" in
 restart)
        dbs_stop
        dbs_start
        ;;
 start)
        dbs_start
        ;;
 status)
        dbs_status
        ;;
 stop)
        dbs_stop
        ;;
 *)
        echo \$"Usage: \$0 {start|stop|status|restart}"
        exit 1
        ;;
esac

exit \$RETVAL
DBS_INIT_EOF
chmod a+x %{i}/Servers/JavaServer/bin/dbs_init.sh

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
#echo "$MYSQL_ROOT/bin/mysql -udbs -pcmsdbs --socket=$MYSQL_SOCK"
echo "$DBS_SCHEMA_ROOT/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql"
# DBS uses trigger which requires to have SUPER priveleges, so we'll create DB using root
# and delegate this to dbs account.
$MYSQL_ROOT/bin/mysql -uroot -pcms --socket=$MYSQL_SOCK < $DBS_SCHEMA_ROOT/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql
$MYSQL_ROOT/bin/mysql --socket=$MYSQL_SOCK -uroot -pcms mysql -e "GRANT ALL ON ${DBS_SCHEMA_VERSION}.* TO dbs@localhost;"

# I need to copy/deploy DBS.war file into tomcat area
cp $DBS_SERVER_ROOT/Servers/JavaServer/DBS.war $APACHE_TOMCAT_ROOT/webapps

# Fix path in dbs_init.sh file since now we know install area
cat $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh | sed "s,rpm_install_area,$RPM_INSTALL_PREFIX,g" > \
    $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh.new
/bin/mv -f $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh.new $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh
echo "+++ Fix path in dbs_init.sh"
chmod a+x $DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh

# time to start up tomcat for user
#$APACHE_TOMCAT_ROOT/bin/catalina.sh start

# kill running mysql|tomcat under my account since build is over
echo "+++ Clean-up mysqld|tomcat processes"
#ps -w -w -f -u`whoami` | egrep "mysqld|tomcat" | grep -v egrep | awk '{print "kill -9 "$2""}'
#ps -w -w -f -u`whoami` | egrep "mysqld|tomcat" | grep -v egrep | awk '{print "kill -9 "$2""}' |/bin/sh
killall -q mysqld
killall -q tomcat

echo
echo
echo "#####  IMPORTANT!!!  #####"
echo "To work with DBS you need to source init.sh file located at"
echo "$DBS_SERVER_ROOT/etc/profile.d/init.sh"
echo
echo "OR use init script to start|stop|status DBS services:"
echo "$DBS_SERVER_ROOT/Servers/JavaServer/bin/dbs_init.sh"
echo "init script file can be placed into /etc/init.d/ to allow auto-startup of DBS service"
echo "##########################"
echo

