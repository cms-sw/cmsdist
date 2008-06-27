### RPM external mysql-deployment 0.0.3

Source: mysql-deployment.sh
Requires: mysql
# Let's fake the fact that we have perl (DBI) so that rpm does not complain.
Provides: mysql-deployment.sh

%prep
mkdir -p %{i}/bin
cat << \EOF > %{i}/bin/mysql-deployment.sh
#!/bin/bash
set -e

if [ -z ${VO_CMS_SW_DIR} ]; then
    echo "+++ Your CMS environment is not setup, missing VO_CMS_SW_DIR environment"
    exit 1
fi
if [ -z ${MYSQL_ROOT} ]; then
    echo "+++ Your CMS MYSQL environment is not setup, MYSQL_ROOT environment"
    exit 1
fi
MYSQL_PATH=$MYSQL_ROOT/mysqldb
if [ ! -d ${MYSQL_PATH} ]; then
    echo "+++ Making ${MYSQL_PATH} directory ..."
    mkdir -p ${MYSQL_PATH}
fi
MYSQL_PORT=3316
MYSQL_SOCK=$MYSQL_PATH/mysql.sock
MYSQL_PID=$MYSQL_PATH/mysqld.pid
MYSQL_ERR=$MYSQL_PATH/error.log

pid=`ps -u ${LOGNAME} | grep mysqld_safe | grep -v grep | tail -1 | awk '{print $1}'`
if [ ! -z ${pid} ]; then
    echo "CMS MySQL server is already running ..."
else
# may use --skip-networking for pure local MySQL

    if [ ! -d $MYSQL_ROOT/mysqldb/mysql ]; then
        echo "+++ Installing CMS MySQL accounts and DBs ..."
        $MYSQL_ROOT/bin/mysql_install_db --datadir=$MYSQL_PATH --port=$MYSQL_PORT --socket=$MYSQL_SOCK

        echo "+++ Start up CMS MySQL daemon on port ${MYSQL_PORT} ..."
        $MYSQL_ROOT/bin/mysqld_safe --datadir=$MYSQL_PATH --port=$MYSQL_PORT \
        --socket=$MYSQL_SOCK --log-error=$MYSQL_ERR --pid-file=$MYSQL_PID &
        
        sleep 10
        # create CMS MySQL root account
        echo "+++ Creating MySQL default root account ..."
        echo "+++ Account for localhost"
        $MYSQL_ROOT/bin/mysqladmin --port=$MYSQL_PORT --socket=$MYSQL_SOCK -u root password "cms"
        echo "+++ Account for `hostname`"
        $MYSQL_ROOT/bin/mysqladmin --port=$MYSQL_PORT --socket=$MYSQL_SOCK -u root -h `hostname` password "cms"

        # create CMS MySQL DBS account
        echo "+++ Creating MySQL default dbs account ..."
        $MYSQL_ROOT/bin/mysql --socket=$MYSQL_SOCK -uroot -pcms mysql -e "CREATE USER dbs@localhost IDENTIFIED BY 'cmsdbs';"
        $MYSQL_ROOT/bin/mysql --socket=$MYSQL_SOCK -uroot -pcms mysql -e "UPDATE user set Select_priv='Y',Insert_priv='Y',Update_priv='Y',Delete_priv='Y',Create_priv='Y',Drop_priv='Y',References_priv='Y',Index_priv='Y',Alter_priv='Y',Create_tmp_table_priv='Y',Lock_tables_priv='Y',Execute_priv='Y',Create_view_priv='Y',Show_view_priv='Y',Create_routine_priv='Y',Alter_routine_priv='Y' where User='dbs';"
    else
        echo "+++ Start up CMS MySQL daemon on port ${MYSQL_PORT} ..."
        $MYSQL_ROOT/bin/mysqld_safe --datadir=$MYSQL_PATH --port=$MYSQL_PORT \
        --socket=$MYSQL_SOCK --log-error=$MYSQL_ERR --pid-file=$MYSQL_PID &
        sleep 10
    fi
fi

EOF
chmod a+x %{i}/bin/mysql-deployment.sh

%build

%install
#cp /tmp/mysql-deployment.sh %{i}/bin
#cp %{i}/mysql-deployment.sh $RPM_SOURCE_DIR

%post
%{relocateConfig}/bin/mysql-deployment.sh

