### RPM external mongo 1.4.2
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

Provides: libpcap.so.0.8.3
# 64-bit versions
Provides: libpcap.so.0.8.3()(64bit)
Source: http://downloads.mongodb.org/src/mongodb-src-r%{realversion}.tar.gz
Requires: boost scons pcre spidermonkey

%prep
%setup -n mongodb-src-r%{realversion}

%build
export CXX=$GCC_ROOT/bin/g++
#scons --64 --cxx=$CXX --extrapath=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT all
scons --64 --cxx=$CXX --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT all

%install
export CXX=$GCC_ROOT/bin/g++
#scons --64 --cxx=$CXX --extrapath=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install
scons --64 --cxx=$CXX --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install

mkdir -p %{i}/{db,logs}

# create mongo init script
mkdir -p %{i}/etc/profile.d/
cat > %{i}/etc/profile.d/mongo_init.sh << MONGO_INIT_EOF
#!/bin/sh
export MYAREA=rpm_install_area
export SCRAM_ARCH=scram_arch
export APT_VERSION=apt_version
source \$MYAREA/\$SCRAM_ARCH/external/apt/\$APT_VERSION/etc/profile.d/init.sh 
source \$MYAREA/%{pkgrel}/etc/profile.d/init.sh

function mongo_stop() 
{
    me=\`whoami\`
    echo $"Stop mongo running under \$me account..."
    ps -w -w -f -u\$me | grep mongod | grep -v grep | awk '{print "kill -9 "\$2""}'|/bin/sh
}
function mongo_start()
{
    echo "+++ Start up MongoDB daemon ..."
    \$MONGO_ROOT/bin/mongod --dbpath=\$MONGO_ROOT/db --quiet 2>&1 1>& \
    \$MONGO_ROOT/logs/mongo.log < /dev/null &
    sleep 2
    echo
    echo "Mongo service is ready ..."
}
function mongo_status() 
{
    me=\`whoami\`
    mongo=\`ps -w -w -f -u\$me | egrep "mongod" | grep -v egrep | wc -l\`
    if [ \${mongo} -ne 1 ]; then
       echo "MongoDB server is not running"
       exit 1
    fi
    ps -w -w -f -u\$me | egrep "mongod" | grep -v egrep | awk '{print "MongoDB server running, pid="\$2""}'
    echo "For more information please have a look at mongo.log:"
    echo "\$MONGO_ROOT/logs/mongo.log"
}

RETVAL=\$?

case "\$1" in
 restart)
        mongo_stop
        mongo_start
        ;;
 start)
        mongo_start
        ;;
 status)
        mongo_status
        ;;
 stop)
        mongo_stop
        ;;
 *)
        echo \$"Usage: \$0 {start|stop|status|restart}"
        exit 1
        ;;
esac

exit \$RETVAL
MONGO_INIT_EOF
chmod a+x %{i}/etc/profile.d/mongo_init.sh

# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
mkdir -p $MONGO_ROOT/db

# Fix path in mongo_init.sh file since now we know install area
cat $MONGO_ROOT/etc/profile.d/mongo_init.sh | sed "s,rpm_install_area,$RPM_INSTALL_PREFIX,g" | \
    sed "s,scram_arch,$SCRAM_ARCH,g" | \
    sed "s,apt_version,$APT_VERSION,g" > \
    $MONGO_ROOT/etc/profile.d/mongo_init.sh.new
/bin/mv -f $MONGO_ROOT/etc/profile.d/mongo_init.sh.new $MONGO_ROOT/etc/profile.d/mongo_init.sh
echo "+++ Fix path in mongo_init.sh"
chmod a+x $MONGO_ROOT/etc/profile.d/mongo_init.sh


