### RPM cms das V01_04_14
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
## INITENV +PATH PYTHONPATH $WMCORE_ROOT/src/python
## INITENV +PATH PYTHONPATH %i/src/python
## INITENV +PATH PYTHONPATH $ELEMENTTREE_ROOT/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV +PATH PYTHONPATH $DAS_ROOT/src/python

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=COMP/DAS&nocache=true&export=DAS&tag=-r%{cvstag}&output=/das.tar.gz
Requires: python cherrypy py2-cheetah sqlite py2-pysqlite py2-sqlalchemy yui elementtree memcached py2-memcached couchdb wmcore

%prep
%setup -n DAS
%build

%install
mkdir -p %{i}/bin
mkdir -p %{i}/test
mkdir -p %{i}/src
mkdir -p %{i}/logs
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/etc/init.d
cp -r bin doc etc src test %i

# copy init script
cp bin/das_web %{i}/etc/init.d
chmod a+x %{i}/etc/init.d/*

# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
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

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
# setup approripate links and made post install procedure
export HOSTNAME=`hostname`
export IP=`host $HOSTNAME | awk '{print $4}'`
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh

cat $DAS_ROOT/etc/das.cfg |  sed "s,^dir =.*,dir = $DAS_ROOT/cache,g" |\
sed "s,logdir = /tmp,logdir = $DAS_ROOT/logs,g" |\
sed "s,http://localhost,http://$IP,g" > $DAS_ROOT/etc/das.cfg.tmp
/bin/mv -f $DAS_ROOT/etc/das.cfg.tmp $DAS_ROOT/etc/das.cfg

cat $DAS_ROOT/src/python/DAS/web/das_cacheconfig.py | sed "s,127.0.0.1,$IP,g" >\
$DAS_ROOT/src/python/DAS/web/das_cacheconfig.py.tmp
/bin/mv -f $DAS_ROOT/src/python/DAS/web/das_cacheconfig.py.tmp $DAS_ROOT/src/python/DAS/web/das_cacheconfig.py

cat $DAS_ROOT/src/python/DAS/web/das_webconfig.py | sed "s,127.0.0.1,$IP,g" |\
sed "s,http://localhost,http://$IP,g" > \
$DAS_ROOT/src/python/DAS/web/das_webconfig.py.tmp
/bin/mv -f $DAS_ROOT/src/python/DAS/web/das_webconfig.py.tmp $DAS_ROOT/src/python/DAS/web/das_webconfig.py
