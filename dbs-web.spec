### RPM cms dbs-web V03_07_00
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

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

# here I use octal code \044 for $ sign since I want "$NAME" to be appear in 
# init.sh file, instead of interpreting it here.
(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $CHERRYPY_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_CHEETAH_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PYSQLITE_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.sh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.sh"; \
 echo "source $YUI_ROOT/etc/profile.d/init.sh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_CX_ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $ELEMENTTREE_ROOT/etc/profile.d/init.sh"; \
 echo -e "export PYTHONPATH=\044PYTHONPATH:\044ELEMENTTREE_ROOT/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/"; \
 echo -e "export DDHOME=\044DBS_WEB_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages"; \
 echo -e "export TNS_ADMIN=\044DDHOME"; \
 echo -e "export DBS_DBPARAM=\044DDHOME/DBParam"; \
 echo -e "export PYTHONPATH=\044DDHOME:\044DDHOME/QueryBuilder:\044PYTHONPATH"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $CHERRYPY_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_CHEETAH_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PYSQLITE_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_MYSQLDB_ROOT/etc/profile.d/init.csh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.csh"; \
 echo "source $YUI_ROOT/etc/profile.d/init.csh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_CX_ORACLE_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $ELEMENTTREE_ROOT/etc/profile.d/init.csh"; \
 echo -e "setenv PYTHONPATH \044{PYTHONPATH}:\044{ELEMENTTREE_ROOT}/share/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages"; \
 echo -e "setenv DDHOME \044DBS_WEB_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages"; \
 echo -e "setenv TNS_ADMIN \044DDHOME"; \
 echo -e "setenv DBS_DBPARAM \044DDHOME/DBParam"; \
 echo -e "setenv PYTHONPATH \044{DDHOME}:\044{DDHOME}/QueryBuilder:\044{PYTHONPATH}"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

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


