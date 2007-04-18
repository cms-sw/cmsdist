### RPM cms boss BOSS_4_3_2
Requires: gcc-wrapper
## INITENV +PATH PATH %i/bin
## INITENV SET BOSSDIR %i
%define cvstag %v
%define compProjectName BOSS
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{compProjectName}&export=%{compProjectName}&&tag=-r%{cvstag}&output=/%{compProjectName}.tar.gz 
Requires: mysql sqlite uuid monalisa-apmon xerces-c
%prep
%setup -n %{compProjectName}
%build
## IMPORT gcc-wrapper
export mysql_dir=$MYSQL_ROOT
export sqlite_dir=$SQLITE_ROOT
echo %{v} > ./VERSION
./configure --prefix=%{i} --with-monalisa-dir=$MONALISA_APMON_ROOT --with-uuid-lib=$UUID_ROOT/lib --with-uuid-include=$UUID_ROOT/include/uuid/ --with-xercesc-lib=$XERCES_C_ROOT/lib --with-xercesc-include=$XERCES_C_ROOT/include
make
%install
make install
mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
 echo "source $UUID_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $SQLITE_ROOT/etc/profile.d/init.sh"; \
 echo "source $XERCES_C_ROOT/etc/profile.d/init.sh"; \
 echo "source $MONALISA_APMON_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $UUID_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $SQLITE_ROOT/etc/profile.d/init.csh"; \
 echo "source $XERCES_C_ROOT/etc/profile.d/init.csh"; \
 echo "source $MONALISA_APMON_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}bossenv.csh
%{relocateConfig}bossenv.sh
