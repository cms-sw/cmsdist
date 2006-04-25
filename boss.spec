### RPM cms boss BOSS_4_0_1
## INITENV +PATH PATH %i/bin
%define cvstag %v
%define compProjectName BOSS
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{compProjectName}&export=%{compProjectName}&&tag=-r%{cvstag}&output=/%{compProjectName}.tar.gz 
Requires: mysql sqlite uuid monalisa-apmon
%prep
%setup -n %{compProjectName}
%build
export mysql_dir=$MYSQL_ROOT
export sqlite_dir=$SQLITE_ROOT
./configure --prefix=%{i} --with-monalisa-dir=$MONALISA_APMON_ROOT --with-uuid-lib=$UUID_ROOT/lib --with-uuid-include=$UUID_ROOT/include/uuid/
make
%install
make install
