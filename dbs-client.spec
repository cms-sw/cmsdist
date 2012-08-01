### RPM cms dbs-client DBS_2_1_7
## INITENV +PATH PYTHONPATH %i/lib/
## INITENV +PATH PYTHONPATH %i/bin/
## INITENV +PATH PYTHONPATH %{i}/lib/
## INITENV +PATH PYTHONPATH %{i}/lib/DBSAPI/
## INITENV SET DBS_CLIENT_CONFIG %{i}/lib/DBSAPI/dbs.config
## INITENV SET DBSCMD_HOME %{i}/lib/DBSAPI

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:/local/reps/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=DBS/Clients/Python&nocache=true&export=DBS&tag=-r%{cvstag}&output=/dbs-client.tar.gz
Requires: python openssl py2-zsi py2-pyxml


%prep
%setup -n DBS
%build
%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d
cp -r Clients/Python/* %{i}/lib/
mv %{i}/lib/bin/* %{i}/bin/
find %i -depth -type d -name CVS -exec rm -fr {} \;
python -m compileall %i/lib || true

#cp -r Clients/Python/DBSAPI/dbsCommandLine.py %{i}/bin/dbs
#chmod a+x %{i}/bin/dbs

(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_ZSI_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_ZSI_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_PYXML_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="dbs-client" version="%v">
    <client>
      <environment name="DBS_CLIENT_BASE" default="%i"/>
    </client>
    <runtime name="PATH" value="$DBS_CLIENT_BASE/bin" type="path"/>
    <runtime name="PYTHONPATH" value="$DBS_CLIENT_BASE/lib" type="path"/>
    <runtime name="PYTHONPATH" value="$DBS_CLIENT_BASE/lib/DBSAPI" type="path"/>
    <runtime name="DBS_CLIENT_CONFIG" value="$DBS_CLIENT_BASE/lib/DBSAPI/dbs.config"/>
    <runtime name="DBSCMD_HOME" value="$DBS_CLIENT_BASE/lib/DBSAPI"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}etc/scram.d/%n.xml

# hack init.csh to get around bug in current version of PKGTOOLS
# will have no effect with the bug fixed verion
perl -p -i -e 's|\. |source |' $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
