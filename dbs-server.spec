### RPM cms dbs-web v00_00_06
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Servers/JavaServer&export=DBS/Servers/JavaServer&tag=-r%{cvstag}&output=/dbs-server.tar.gz
Requires: python dbs-client py2-sqlalchemy cherrypy mysql py2-mysqldb oracle py2-cx-oracle apache-tomcat

%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/Servers/JavaServer )

%install
mkdir -p %i/bin
mkdir -p %i/lib/python
cp -r Servers/JavaServer/* %i/lib/python

