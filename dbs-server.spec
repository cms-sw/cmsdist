### RPM cms dbs-server DBS_2_0_2

%define cvstag %{realversion}
# define version of DBS to use, it's schema version
%define dbs_version %{realversion}

Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: apache-ant mysql mysql-deployment oracle apache-tomcat java-jdk dbs-schema dbs-libs

%prep
%setup -n DBS
# kill running mysql|tomcat under my account since build is over
ps -w -w -f -u`whoami` | egrep "mysqld|tomcat" | grep -v egrep | awk '{print "kill -9 "$2""}' |/bin/sh

%build
# DBS wants to have LibValut attached to DBS top-level dir, required by build.xml file
ln -s $DBS_LIBS_ROOT/lib LibValut
echo "PWD=$PWD"
cd Servers/JavaServer

# retrieve which DBS schema to use
#export DBS_SCHEMA=`grep "^use " $DBS_SCHEMA_ROOT/lib/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql | awk '{print $2}' | sed "s/;//g"`
#export DBS_SCHEMA_VERSION=`cat  $DBS_SCHEMA_ROOT/lib/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql | grep "INSERT INTO SchemaVersion" | awk '{split($0,a,"\x27"); print a[2]}'`

# fix context.xml file
cat etc/context.xml.tobe  | sed "s/__insert_username__/dbs/g" | sed "s/__insert_password__/cmsdbs/g" | sed "s/3306/3316/g" | sed "s/maxActive=\"0\"/maxActive=\"100\"/g" > etc/context.xml

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

# copy war file
cp %{i}/Servers/JavaServer/DBS.war $APACHE_TOMCAT_ROOT/webapps

# create dbs init script
mkdir -p %{i}/Servers/JavaServer/bin
cat > %{i}/Servers/JavaServer/bin/dbs_init.sh << DBS_INIT_EOF
#!/bin/sh
export MYAREA=rpm_install_area
export SCRAM_ARCH=slc4_ia32_gcc345
source \$MYAREA/\$SCRAM_ARCH/external/apt/\$APT_VERSION/etc/profile.d/init.sh 
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
    --socket=\$MYSQL_SOCK --log-error=\$MYSQL_ERR --pid-file=\$MYSQL_PID --max_allowed_packet=32M &
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
echo "+++ Grand permission to dbs account, DBS schema %{dbs_version} ..."
#echo "$MYSQL_ROOT/bin/mysql -udbs -pcmsdbs --socket=$MYSQL_SOCK"
echo "$DBS_SCHEMA_ROOT/lib/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql"
# DBS uses trigger which requires to have SUPER priveleges, so we'll create DB using root
# and delegate this to dbs account.
export DBS_SCHEMA=`grep "^use " $DBS_SCHEMA_ROOT/lib/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql | awk '{print $2}' | sed "s/;//g"`
$MYSQL_ROOT/bin/mysql -uroot -pcms --port=$MYSQL_PORT --socket=$MYSQL_SOCK < $DBS_SCHEMA_ROOT/lib/Schema/NeXtGen/DBS-NeXtGen-MySQL_DEPLOYABLE.sql
$MYSQL_ROOT/bin/mysql --socket=$MYSQL_SOCK --port=$MYSQL_PORT -uroot -pcms mysql -e "GRANT ALL ON ${DBS_SCHEMA}.* TO dbs@localhost;"

# I need to copy/deploy DBS.war file into tomcat area
cp $DBS_SERVER_ROOT/Servers/JavaServer/DBS.war $APACHE_TOMCAT_ROOT/webapps

# Copy mysql jdbc driver to tomcat
cp -f $DBS_LIBS_ROOT/lib/*.jar $APACHE_TOMCAT_ROOT/common/lib

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
#killall -q mysqld
#cat $MYSQL_ROOT/mysqldb/mysqld.pid
$MYSQL_ROOT/bin/mysqladmin -uroot -pcms --socket=$MYSQL_SOCK --port=3316 shutdown
killall -q tomcat

# made correct link to LibValut
rm -f $DBS_SERVER_ROOT/LibValut
ln -s $DBS_LIBS_ROOT/lib $DBS_SERVER_ROOT/LibValut

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

