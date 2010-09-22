### RPM cms das 0.5.2
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
## INITENV +PATH PYTHONPATH $WMCORE_ROOT/src/python
## INITENV +PATH PYTHONPATH %i/src/python
## INITENV +PATH PYTHONPATH $ELEMENTTREE_ROOT/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV +PATH PYTHONPATH $DAS_ROOT/src/python

%define arch `uname -p`
%define pver `echo $PYTHON_VERSION | cut -d. -f1,2`

#%define cvstag %{realversion}
#%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
#Source: %cvsserver&strategy=checkout&module=COMP/DAS&nocache=true&export=DAS&tag=-r%{cvstag}&output=/das.tar.gz

%define svnserver svn://svn.cern.ch/reps/CMSDMWM/DAS/tags/%{realversion}
Source: %svnserver?scheme=svn+ssh&strategy=export&module=DAS&output=/das.tar.gz

Requires: python cherrypy py2-cheetah yui elementtree mongo py2-pymongo py2-cjson py2-yaml wmcore py2-sphinx py2-openid py2-sqlalchemy py2-ipython py2-pystemmer py2-mongoengine py2-lxml py2-ply

%prep
%setup -n DAS
%build
python setup.py build
cp build/lib.linux-%{arch}-%{pver}/DAS/extensions/das_speed_utils.so src/python/DAS/extensions/

%install
mkdir -p %{i}/bin
mkdir -p %{i}/test
mkdir -p %{i}/src
mkdir -p %{i}/logs
mkdir -p %{i}/doc/sphinx/{_static,_templates,_images}
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/etc/init.d
cp -r bin doc etc src test %i

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
export IP=`host $HOSTNAME | awk '{print $4}'` | head -1
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh

# make appropriate links to DAS services
#ln -s $DAS_ROOT/bin/das_web $DAS_ROOT/etc/init.d/das_web
#ln -s $DAS_ROOT/bin/das_map $DAS_ROOT/etc/init.d/das_map
#ln -s $DAS_ROOT/bin/das_cacheserver $DAS_ROOT/etc/init.d/das_cacheserver
ln -s $DAS_ROOT/bin/das_server $DAS_ROOT/etc/init.d/das_server

cat $DAS_ROOT/etc/das.cfg |  sed "s,^dir =.*,dir = $DAS_ROOT/cache,g" |\
sed "s,logdir = /tmp,logdir = $DAS_ROOT/logs,g" |\
sed "s,http://localhost,http://$IP,g" > $DAS_ROOT/etc/das.cfg.tmp
/bin/mv -f $DAS_ROOT/etc/das.cfg.tmp $DAS_ROOT/etc/das.cfg

#cat $DAS_ROOT/src/python/DAS/web/das_cacheconfig.py | sed "s,127.0.0.1,$IP,g" >\
#$DAS_ROOT/src/python/DAS/web/das_cacheconfig.py.tmp
#/bin/mv -f $DAS_ROOT/src/python/DAS/web/das_cacheconfig.py.tmp $DAS_ROOT/src/python/DAS/web/das_cacheconfig.py

#cat $DAS_ROOT/src/python/DAS/web/das_webconfig.py | sed "s,127.0.0.1,$IP,g" |\
#sed "s,http://localhost,http://$IP,g" > \
#$DAS_ROOT/src/python/DAS/web/das_webconfig.py.tmp
#/bin/mv -f $DAS_ROOT/src/python/DAS/web/das_webconfig.py.tmp $DAS_ROOT/src/python/DAS/web/das_webconfig.py

# build DAS sphinx documentation
cd $DAS_ROOT/doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

