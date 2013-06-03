### RPM cms webconddb 1.7.3
## INITENV +PATH PYTHONPATH %i
## INITENV SET WEBCONDDB_CONFIG %i/Controllers/IOVManagement/conddbpage.conf
%define moduleName WEBCONDDB
%define exportName WEBCONDDB
%define cvstag WebCondDB-1-7-3
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/WEBCONDDB.tar.gz
Requires: python py2-pysqlite cherrypy py2-cheetah yui sqlite py2-formencode zlib expat openssl bz2lib db4 gdbm webtools py2-pycrypto py2-matplotlib py2-simplejson


%prep
%setup -n WEBCONDDB 
%build
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d/
rm -rf %i/etc/init.d 
mkdir -p %i/etc/init.d/

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

cp -r CondDB/Controllers %i
cp -r CondDB/scripts %i
cp -f CondDB/scripts/webconddb %i/etc/init.d/
cp -f CondDB/scripts/webconddb.conf %i/etc/init.d/
chmod a+x %{i}/etc/init.d/webconddb

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
echo "*************************************************************"
echo Please now change the following config files if necessary:
echo
echo $RPM_INSTALL_PREFIX/%{pkgrel}/Controllers/CondDBCommon/config/condDBCommon.ini
echo
echo $RPM_INSTALL_PREFIX/%{pkgrel}/etc/init.d/webconddb.conf
echo "*************************************************************"
