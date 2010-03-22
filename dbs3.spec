### RPM cms dbs3 DBS_3_S3_0_pre1
## INITENV +PATH PYTHONPATH %i/Server/Python/src
## INITENV SET DBS3_SERVER_ROOT %i/Server/Python

%define cvsver %v
%define configdir Config
%define instance cms_dbs
%define serverlogsdir Logs
%define service DBS
%define dburl oracle://user:passwd@db
%define dbowner schemaowner
%define dbsver DBS_3_0_0

Requires: wmcore-webtools wmcore-db-oracle py2-cjson py2-mysqldb
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true&module=COMP/DBS/DBS3&export=%{n}&tag=-r%{cvsver}&output=/%{n}.tar.gz

%prep
%setup -n %{n}

%build

%install
cp -rp %_builddir/%{n}/* %i/
mkdir -p %{i}/%{configdir}
mkdir -p %{i}/%{serverlogsdir}

#----------------------------------------
# Generates the script used to start dbs3
cat << \EOF > %i/setup.sh

if [ -z "$DBS3_ROOT" ]; then
       source ./etc/profile.d/init.sh
fi

export MYSQL_UNIX_PORT=$MYSQL_ROOT/mysqldb/mysql.sock

dbs3_start1(){
if [ -z "$1" ]
   then
       $WMCORE_ROOT/src/python/WMCore/WebTools/Root.py -i $DBS3_ROOT/%{configdir}/%{instance}.py
   else
       $WMCORE_ROOT/src/python/WMCore/WebTools/Root.py -i $DBS3_ROOT/%{configdir}/$1.py
fi
}

dbs3start(){
if [ -z "$1" ]   
   then
       dbs3_start1 1>/dev/null 2>&1 &
   else
       dbs3_start1 $1 1>/dev/null 2>&1 &
fi
}

EOF

#---------------------------
# Generates DBS config file
cat << \EOF > %{i}/%{configdir}/%{instance}.py
"""
DBS Server  configuration file
"""
import os, logging
from WMCore.Configuration import Configuration

config = Configuration()

config.component_('Webtools')
config.Webtools.port = 8585
config.Webtools.host = '::'
config.Webtools.access_log_file = os.environ['DBS3_ROOT'] +"/%{serverlogsdir}/%{instance}.log"
config.Webtools.error_log_file = os.environ['DBS3_ROOT'] +"/%{serverlogsdir}/%{instance}.log"
config.Webtools.log_screen = True
config.Webtools.application = '%{instance}'

config.component_('%{instance}')
config.%{instance}.templates = os.environ['WMCORE_ROOT'] + '/src/templates/WMCore/WebTools'
config.%{instance}.title = 'DBS Server'
config.%{instance}.description = 'CMS DBS Service'
config.%{instance}.admin = 'yourname'

config.%{instance}.section_('views')

active=config.%{instance}.views.section_('active')
active.section_('%{service}')
active.%{service}.object = 'WMCore.WebTools.RESTApi'
active.%{service}.section_('model')
active.%{service}.model.object = 'dbs.web.DBSReaderModel'
active.%{service}.section_('formatter')
active.%{service}.formatter.object = 'WMCore.WebTools.RESTFormatter'

active.%{service}.database = '%{dburl}'
active.%{service}.dbowner = '%{dbowner}'
active.%{service}.version = '%{dbsver}'

EOF

#-----------------------------------
# Generates DBS config file (writer)
sed -e 's/%{instance}.log/%{instance}_writer.log/g' -e 's/DBSReaderModel/DBSWriterModel/g' \
  < %{i}/%{configdir}/%{instance}.py > %{i}/%{configdir}/%{instance}_writer.py

#--------------------------------------------------------------------
# The following lines (including relocation ones in the post section) 
# are necessary to correctly setup the environment.
rm -rf %i/etc/profile.d
# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
  
