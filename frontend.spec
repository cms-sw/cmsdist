### RPM cms frontend 1.0

# Dummy package to get apache-conf installed.
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rSERVER_CONF_1_12&output=/config.tar.gz
Source1: %cvsserver&module=COMP/WEBTOOLS/WelcomePages&export=htdocs&tag=-rSERVER_CONF_1_12&output=/htdocs.tar.gz
Requires: apache2-conf

%prep
%setup -T -b 0 -n conf
%setup -D -T -b 1 -n htdocs

%build
%install
