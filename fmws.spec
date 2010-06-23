### RPM cms fmws 0.10.4
## INITENV +PATH PYTHONPATH %i/lib/
## INITENV +PATH PYTHONPATH $ELEMENTTREE_ROOT/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV SET FMWSHOME $FMWS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV SET PYTHONPATH ${FMWSHOME}:${PYTHONPATH}

####%define cvstag %{realversion}
%define moduleName FILEMOVER
%define exportName FILEMOVER
%define cvstag V01_00_26
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
####Source: http://t2.unl.edu/store/CmsFileServer-%{realversion}.tar.gz
Source: %cvsserver&strategy=checkout&module=COMP/%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python openssl cherrypy py2-cheetah webtools yui java-jdk srmcp elementtree webtools-base mongo py2-pymongo

%prep
%setup -n %{moduleName}
%build

%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/etc/init.d
pyver=`echo $PYTHON_VERSION | cut -d. -f1,2`
mkdir -p %i/lib/python$pyver/site-packages
cp -r src/CmsFileServer/* %i/lib/python$pyver/site-packages
cp    etc/fmws_init* %{i}/etc/init.d
cp    etc/*.sh %{i}/etc/init.d/
chmod a+x %{i}/etc/init.d/*

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=dbs-client version=%v>
<client>
 <Environment name=FMWS_BASE default="%i"></Environment>
</client>
<Runtime name=PATH value="$FMWS_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

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
%{relocateConfig}etc/scram.d/%n

. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
mkdir -p $FMWSHOME/{logs,css}
if [ -d /data/download ]; then
   ln -s /data/download $FMWSHOME/download
else
   mkdir -p $FMWSHOME/download
fi
cd $FMWSHOME
./scripts/genTemplates.sh
site="local"
if  [ ! -z `hostname | grep cern.ch` ]; then
    site="CERN"
elif [ ! -z `hostname | grep fnal.gov` ]; then
    site="FNAL"
fi
./FMWSConfig.py --config=$site

# create new crontab
echo "0 0,3,6,9,12,15,18,21 * * * $RPM_INSTALL_PREFIX/%{pkgrel}/etc/init.d/renew_proxy.sh 2>&1 1>& $RPM_INSTALL_PREFIX/%{pkgrel}/proxy.cron" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/init.d/cronjob.sh
echo "0 8 26 4 * $RPM_INSTALL_PREFIX/%{pkgrel}/etc/init.d/notify_operator.sh 2>&1 1>& $RPM_INSTALL_PREFIX/%{pkgrel}/userproxy.cron" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/init.d/cronjob.sh
chmod a+x $RPM_INSTALL_PREFIX/%{pkgrel}/etc/init.d/cronjob.sh

