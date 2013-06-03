### RPM cms dbs-light DBS_1_0_8_pre2
## INITENV +PATH PYTHONPATH %i/lib/Clients/Python

# in order to build DBS RPM you MUST specify which schema/client version should be used.
%define schemaVer DBS_1_0_7
%define clientVer DBS_1_0_7

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS&export=DBS&tag=-r%{cvstag}&output=/dbs-light.tar.gz
#Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/{Servers/JavaServer,Clients/Python,Schema/NeXtGen/DBS-NeXtGen-SQLite_DEPLOYABLE.sql}&export=DBS&tag=-r%{cvstag}&output=/dbs-light.tar.gz
Requires: python openssl apache-ant sqlite java-jdk
#Requires: apache-ant mysql oracle apache-tomcat 

%prep
%setup -n DBS

%build
echo "PWD=$PWD"
env | grep JAVA
export JAVA_HOME=$JAVA_JDK_ROOT
# server
cd Servers/JavaServer
echo "PWD=$PWD"
ant --noconfig jar
cd ../../
# client
(make DBSHOME=%_builddir/DBS/Clients/Python )
# schema
(make DBSHOME=%_builddir/DBS/Schema/NeXtGen )

%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib

# client
mkdir -p %{i}/Clients/Python
cp -r Clients/Python/DBSAPI %{i}/Clients/Python

# schema
ls -l Schema/NeXtGen
mkdir -p %{i}/Schema/NeXtGen
cp -r Schema/NeXtGen/DBS-NeXtGen-SQLite_DEPLOYABLE.sql  %{i}/Schema/NeXtGen/
 
# server
mkdir -p %{i}/Servers/JavaServer/

mkdir -p %{i}/etc/profile.d
(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $SQLITE_ROOT/etc/profile.d/init.sh"; \
 echo "source $APACHE_ANT_ROOT/etc/profile.d/init.sh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.sh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.sh"; \
 echo -e "export PYTHONPATH=\044PYTHONPATH:\044DBS_LIGHT_ROOT/Clients/Python:\044DBS_LIGHT_ROOT/Clients/Python/DBSAPI"; \
 echo -e "export DBS_CLIENT_CONFIG=\044DBS_LIGHT_ROOT/Clients/Python/DBSAPI/dbs.config"; \
 echo -e "export DBS_SERVER_CONFIG=\044DBS_LIGHT_ROOT/Servers/JavaServer/etc/context.xml"; \
 echo -e "export JAVA_HOME=\044JAVA_JDK_ROOT"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $SQLITE_ROOT/etc/profile.d/init.csh"; \
 echo "source $APACHE_ANT_ROOT/etc/profile.d/init.csh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo -e "setenv PYTHONPATH \044PYTHONPATH:\044DBS_LIGHT_ROOT/Clients/Python:\044DBS_LIGHT_ROOT/Clients/Python/DBSAPI"; \
 echo -e "setenv DBS_CLIENT_CONFIG \044DBS_LIGHT_ROOT/Clients/Python/DBSAPI/dbs.config"; \
 echo -e "setenv DBS_SERVER_CONFIG \044DBS_LIGHT_ROOT/Servers/JavaServer/etc/context.xml"; \
 echo -e "setenv JAVA_HOME \044JAVA_JDK_ROOT"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

# compile server code
#cd Servers/JavaServer
#ant --noconfig jar
#ls -l $PWD
#find . -name "*.jar"
#cd ../../
cp -r Servers/JavaServer/* %{i}/Servers/JavaServer

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh

# install DBS stand-along DB
if [ ! -f $RPM_INSTALL_PREFIX/%{pkgrel}/dbs.db ]; then
   sqlite3 $RPM_INSTALL_PREFIX/%{pkgrel}/dbs.db < \
           $RPM_INSTALL_PREFIX/%{pkgrel}/Schema/NeXtGen/DBS-NeXtGen-SQLite_DEPLOYABLE.sql
fi

# correct DBS client config file to operate in stand-along mode
cat $RPM_INSTALL_PREFIX/%{pkgrel}/Clients/Python/DBSAPI/dbs.config | \
sed "s/DBSHOME/#DBSHOME/g" |
sed "s/JAVAHOME/#JAVAHOME/g" |
sed "s/MODE=POST/#MODE=POST/g" > \
    $RPM_INSTALL_PREFIX/%{pkgrel}/Clients/Python/DBSAPI/dbs.config.tmp

#if [ -z $JAVA_HOME ]; then
#   echo "########################## IMPORTANT ##############################"
#   echo "# In order to install DBS code you MUST have JAVA on your machine #"
#   echo "# DBS code relies on JAVA version 1.5.0_10 and above              #"
#   echo "# Please install JAVA and setup JAVA_HOME environtment and re-run #"
#   echo "###################################################################"
#   exit 1
#fi

cat >> $RPM_INSTALL_PREFIX/%{pkgrel}/Clients/Python/DBSAPI/dbs.config.tmp << EOF
# RPM AUTO-CONFIG FOR STANDALONE MODE
MODE=EXEC
DBSHOME=`echo $DBS_LIGHT_ROOT`/Servers/JavaServer
JAVAHOME=`echo $JAVA_HOME`
EOF
mv $RPM_INSTALL_PREFIX/%{pkgrel}/Clients/Python/DBSAPI/dbs.config.tmp \
   $RPM_INSTALL_PREFIX/%{pkgrel}/Clients/Python/DBSAPI/dbs.config

# correct DBS server config file
cat > $RPM_INSTALL_PREFIX/%{pkgrel}/Servers/JavaServer/etc/context.xml << EOF
<Context path="/servlet/DBSServlet" docBase="DBSServlet" debug="5" reloadable="true" crossContext="true">
      <Resource name="jdbc/dbs" 
              auth="Container" 
              type="javax.sql.DataSource" 
              maxActive="0" 
              maxIdle="1" 
              maxWait="-1" 
              username="" 
              password="" 
              driverClassName="org.sqlite.JDBC" 
              url="jdbc:sqlite:`echo $RPM_INSTALL_PREFIX/%{pkgrel}/dbs.db`"/> 
<SupportedSchemaVersion schemaversion="%{schemaVer}" />
<SupportedClientVersions clientversions="%{clientVer}" />
<DBSBlockConfig maxBlockSize="20000" maxBlockFiles="50" />
</Context>
EOF

# obsolete code for reference, since it demonstrates how to do post-install compilation
# Until we will ship proper version of JAVA in CMS RPMs I need this piece
# to install jar file under local site. Compile using local JAVA.
#cd $RPM_INSTALL_PREFIX/%{pkgrel}/Servers/JavaServer/
#ant --noconfig jar
#ls -l $PWD
#find . -name "*.jar"
