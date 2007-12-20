### RPM cms dbs-web V03_08_00
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
#
%define cvstag %v
#Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Web/DataDiscovery&export=DBS/Web/DataDiscovery&tag=-r%{cvstag}&output=/dbs-web.tar.gz
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Web/DataDiscovery&tag=-r%{cvstag}&output=/dbs-web.tar.gz
Requires: python py2-sqlalchemy cherrypy mysql py2-mysqldb oracle py2-cx-oracle sqlite py2-pysqlite py2-cheetah webtools yui elementtree

%prep
%setup -n DBS/Web/DataDiscovery
%build

%install
mkdir -p %{i}/bin
mkdir -p %{i}/etc/profile.d
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
cp -r Web/DataDiscovery/* %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages

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

# here I use octal code \044 for $ sign since I want "$NAME" to be appear in 
# init.sh file, instead of interpreting it here.
# FIXME: why did Valentin not use INITENV metacommand? Shall we add INITENVE to CMSBUILD which does -e???
(echo -e "export PYTHONPATH=\044PYTHONPATH:\044ELEMENTTREE_ROOT/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/"
 echo -e "export DDHOME=\044DBS_WEB_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages"
 echo -e "export TNS_ADMIN=\044DDHOME"
 echo -e "export DBS_DBPARAM=\044DDHOME/DBParam"
 echo -e "export PYTHONPATH=\044DDHOME:\044DDHOME/QueryBuilder:\044PYTHONPATH"
 ) >> %{i}/etc/profile.d/dependencies-setup.sh

(echo -e "setenv PYTHONPATH \044{PYTHONPATH}:\044{ELEMENTTREE_ROOT}/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages";
 echo -e "setenv DDHOME \044DBS_WEB_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages"
 echo -e "setenv TNS_ADMIN \044DDHOME"
 echo -e "setenv DBS_DBPARAM \044DDHOME/DBParam" 
 echo -e "setenv PYTHONPATH \044{DDHOME}:\044{DDHOME}/QueryBuilder:\044{PYTHONPATH}" 
 ) >> %{i}/etc/profile.d/dependencies-setup.csh

# echo -e "rm -f \044DDHOME/YUI"; \
# echo -e "ln -s $YUI_ROOT/build \044DDHOME/YUI"; \
# echo -e "ln -s $WEBTOOLS_ROOT/Controllers \044DDHOME/WEBTOOLS"; \
# Generate python code from templates 
./scripts/genTemplates.sh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
ln -s $YUI_ROOT/build $DDHOME/YUI
ln -s $WEBTOOLS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Controllers $DDHOME/WEBTOOLS
$RPM_INSTALL_PREFIX/%{pkgrel}/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/scripts/post-install.sh `hostname` 8003
