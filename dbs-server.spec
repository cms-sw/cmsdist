### RPM cms dbs-web v01_02_00
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Web/DataDiscovery&export=DBS/Web/DataDiscovery&tag=-r%{cvstag}&output=/dbs-web.tar.gz
Requires: python dbs-client py2-sqlalchemy cherrypy

%prep
%setup -n DBS
%build
(make DBSHOME=%_builddir/DBS/Web/DataDiscovery )

%install
mkdir -p %i/bin
mkdir -p %i/lib/python
ls -l Web/DataDiscovery
cp -r Web/DataDiscovery/* %i/lib/python

