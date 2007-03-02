### RPM cms dbs-server v00_00_14

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: apache-ant mysql oracle apache-tomcat
#Requires: apache-ant apache-tomcat

%prep
%setup -n DBS
%build
echo "PWD=$PWD"
cd Servers/JavaServer
echo "PWD=$PWD"
ant --noconfig dist
cd ../../

%install
mkdir -p %{i}/Servers/JavaServer/
cp -r Servers/JavaServer/* %{i}/Servers/JavaServer

