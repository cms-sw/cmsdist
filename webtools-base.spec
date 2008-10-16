### RPM cms webtools-base 0.1.5
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define moduleName WEBTOOLS
%define exportName WEBTOOLS
%define cvstag V01-03-20
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python cherrypy py2-cheetah yui webtools
Provides: perl(CGI) 
Provides: perl(Crypt::CBC) 
Provides: perl(SecurityModule) 
Provides: perl(DBI)
%prep
%setup -n %{moduleName}
%build

rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done

perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh

%install
mkdir -p %i/etc
mkdir -p %i/bin
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Applications
cp -r Applications/base %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Applications
cp cmsWeb %i/bin


cat << \EOF > %i/bin/base_init
#!/bin/bash
#
# dbs_discovery This script runs CMS DBS Data Discovery service
#
# chkconfig: 345 05 95

if [ -z ${WEBTOOLS_BASE_ROOT} ]; then
   echo $"The WEBTOOLS_BASE_ROOT environment is not set"
   exit 1
fi

RETVAL=$?

port=7999
pid=`ps auxw | grep WSServer | grep -v grep | awk '{print $2}'`
base=base
if [ -n "$WEBTOOLS_BASEURL" ]; then
    url="$WEBTOOLS_BASEURL/$base"
else
    url="http://cmsweb.cern.ch/$base"
fi
cmd="cmsWeb --base-url=$url --port $port --default-page /WSServer"

case "$1" in
 restart)
        echo $"Checking for existing WSServer..."
        if [ ! -z ${pid} ]; then
          kill -9 ${pid}
        fi
        echo $"Restart WSServer..."
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
          echo $"${base} is running, pid=${pid}"
          exit 0
        fi
        echo $"${base} is stopped"
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
chmod a+x %i/bin/base_init

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
perl -p -i -e "s!\@RPM_INSTALL_PREFIX\@!$RPM_INSTALL_PREFIX/%pkgrel!" $RPM_INSTALL_PREFIX/%pkgrel/bin/cmsWeb

