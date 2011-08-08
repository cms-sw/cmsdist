### RPM cms dbs-server DBS_2_1_6

%define cvstag %{realversion}
# define version of DBS to use, it's schema version
%define dbs_version %{realversion}

Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: apache-ant mysql mysql-deployment oracle apache-tomcat java-jdk dbs-schema dbs-libs

%prep
%setup -n DBS

%build
# DBS wants to have LibValut attached to DBS top-level dir, required by build.xml file
ln -s $DBS_LIBS_ROOT/lib LibValut
echo "PWD=$PWD"
cd Servers/JavaServer

# compile DBS server code
mkdir -p bin/WEB-INF/lib
echo "PWD=$PWD"
source $JAVA_JDK_ROOT/etc/profile.d/init.sh
export JAVA_HOME=$JAVA_JDK_ROOT 
ant --noconfig dist
cd ../../

%install
mkdir -p %{i}/Servers/JavaServer/bin/WEB-INF/lib
cp -r Servers/JavaServer/* %{i}/Servers/JavaServer
ln -s $DBS_LIBS_ROOT/lib %{i}/LibValut

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done
 
%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
