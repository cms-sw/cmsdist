### RPM external couchdb 1.0.1

Source0: http://apache.mirror.testserver.li/couchdb/%{realversion}/apache-%n-%{realversion}.tar.gz

# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
Requires: curl spidermonkey openssl icu4c erlang couchapp

%prep
[ "$(md5sum %{SOURCE0} |cut -b1-32)" == "001cf286b72492617e9ffba271702a00" ]
%setup -n apache-%n-%{realversion}

%build
export PATH=$PATH:$ICU4C_ROOT/bin:$ERLANG_ROOT/bin
./configure --prefix=%i --with-js-lib=$SPIDERMONKEY_ROOT/lib --with-js-include=$SPIDERMONKEY_ROOT/include --with-erlang=$ERLANG_ROOT/lib/erlang/usr/include
make

make install
# Modify couchdb script to use env. variables rather then full path
export COUCH_INSTALL_DIR=%i
cp %i/bin/couchdb %i/bin/couchdb.orig
cat %i/bin/couchdb | \
    sed "s,$ICU4C_ROOT,\$ICU4C_ROOT,g" | \
    sed "s,$ERLANG_ROOT,\$ERLANG_ROOT,g" | \
    sed "s,$COUCH_INSTALL_DIR,\$COUCHDB_ROOT,g" \
        > %i/bin/couchdb.new
mv %i/bin/couchdb.new %i/bin/couchdb
ls -l %i/bin/couchdb
   
cp %i/bin/couchjs %i/bin/couchjs.orig
cat %i/bin/couchjs | \
    sed "s,$ICU4C_ROOT,\$ICU4C_ROOT,g" | \
    sed "s,$ERLANG_ROOT,\$ERLANG_ROOT,g" | \
    sed "s,$COUCH_INSTALL_DIR,\$COUCHDB_ROOT,g" \
        > %i/bin/couchjs.new
ls -l %i/bin/couchjs.new
mv %i/bin/couchjs.new %i/bin/couchjs
chmod a+x %i/bin/couch*

mkdir -p %i/etc/init.d
cat << \EOF >%i/etc/init.d/couchdb_init
#!/bin/bash
# chkconfig: 345 05 95

if [ -z ${COUCHDB_ROOT} ]; then
   echo $"The COUCHDB_ROOT environment is not set"
   exit 1
fi

RETVAL=$?

pid=`ps auxw | grep couchdb | grep -v grep | grep -v couchdb_init | awk '{print $2}'`
cmd="$COUCHDB_ROOT/bin/couchdb"

case "$1" in
 restart)
        echo $"Checking for existing CouchDB..."
        if [ ! -z ${pid} ]; then
          kill -9 ${pid}
        fi
        echo $"Restart CouchDB..."
        nohup ${cmd} 2>&1 1>& /dev/null < /dev/null &
        ;;
 start)
        if [ ! -z ${pid} ]; then
          kill -9 ${pid}
        fi
        nohup ${cmd} 2>&1 1>& /dev/null < /dev/null &
        ;;
 status)
        if [ ! -z ${pid} ]; then
          echo $"couchdb is running, pid=${pid}"
          exit 0
        fi
        echo $"couchdb is stopped"
        exit 3
        ;;
 stop)
        if [ ! -z ${pid} ]; then
          kill -9 ${pid}
        fi
        ;;
 *)
        echo $"Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac

exit $RETVAL

EOF
chmod a+x %i/etc/init.d/couchdb_init

%install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Couchdb version=%v>
<lib name=coucndb>
<client>
 <Environment name=COUCHDB_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$COUCHDB_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$COUCHDB_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$COUCHDB_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
# fix couch.ini file to use path on remote node
export COUCH_INSTALL_DIR=%i
if [ -f $COUCHDB_ROOT/etc/couchdb/couch.ini ]; then
cat $COUCHDB_ROOT/etc/couchdb/couch.ini |  \
    sed "s,$COUCH_INSTALL_DIR,$COUCHDB_ROOT,g" > \
    $COUCHDB_ROOT/etc/couchdb/couch.ini.new
mv $COUCHDB_ROOT/etc/couchdb/couch.ini.new $COUCHDB_ROOT/etc/couchdb/couch.ini
fi

if [ -f $COUCHDB_ROOT/etc/couchdb/default.ini ]; then
cat $COUCHDB_ROOT/etc/couchdb/default.ini |  \
    sed "s,$COUCH_INSTALL_DIR,$COUCHDB_ROOT,g" > \
    $COUCHDB_ROOT/etc/couchdb/default.ini.new
mv $COUCHDB_ROOT/etc/couchdb/default.ini.new $COUCHDB_ROOT/etc/couchdb/default.ini
fi

