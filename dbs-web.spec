### RPM cms dbs-web V04_01_19
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
## INITENV +PATH PYTHONPATH $ELEMENTTREE_ROOT/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV SET DDHOME $DBS_WEB_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV SET DBS_DBPARAM $DDHOME/DBParam
## INITENV SET PYTHONPATH ${DDHOME}:${DDHOME}/QueryBuilder:${PYTHONPATH}

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=DBS/Web/DataDiscovery&nocache=true&export=DBS&tag=-r%{cvstag}&output=/dbs-web.tar.gz
Requires: python py2-sqlalchemy cherrypy py2-cheetah webtools yui elementtree dbs-client mysql py2-mysqldb sqlite py2-pysqlite py2-cx-oracle oracle-env

%prep
%setup -n DBS/Web/DataDiscovery
%build

%install
mkdir -p %{i}/bin
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/etc/init.d
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
cp -r * %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages

# copy init script
cp cmsweb_discovery dbs_discovery %{i}/etc/init.d
chmod a+x %{i}/etc/init.d/*

cd %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
#ln -s $YUI_ROOT/build YUI


# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
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

# Generate python code from templates 
./scripts/genTemplates.sh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
ln -s $YUI_ROOT/build $DDHOME/YUI
ln -s $YUI_ROOT $DDHOME/yui
mkdir -p $DDHOME/rss
ln -s $WEBTOOLS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Controllers $DDHOME/WEBTOOLS
pdir=$RPM_INSTALL_PREFIX/%{pkgrel}/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
if [ `hostname` == "cmswttest.cern.ch" ]; then
    ${pdir}/scripts/post-install.sh https://cmsweb.cern.ch/dbs_discovery_wttest 8008
    cat ${pdir}/DBSDD.conf | sed "s/# URL=/URL=/g" | sed "s/# PORT=/PORT=/g" > ${pdir}/DBSDD.conf.tmp
    mv ${pdir}/DBSDD.conf.tmp ${pdir}/DBSDD.conf
else
    ${pdir}/scripts/post-install.sh `hostname` 8003
    cat ${pdir}/DBSDD.conf | sed "s/# URL=/### _url_=/g" | sed "s/# PORT=/### _port_=/g" > ${pdir}/DBSDD.conf.tmp
    mv ${pdir}/DBSDD.conf.tmp ${pdir}/DBSDD.conf
fi
if [ -n "${WEBTOOLS_CONF}" ] && [ -f ${WEBTOOLS_CONF}/dbs/DBParam ]; then
    rm -f ${pdir}/DBParam
    ln -s ${WEBTOOLS_CONF}/dbs/DBParam ${pdir}/DBParam
fi
###export TARGET_PROJECT=dbs-web
