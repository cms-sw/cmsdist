### RPM cms dbs-client DBS_2_1_9
## INITENV +PATH PYTHONPATH %i/lib/
## INITENV +PATH PYTHONPATH %i/bin/
## INITENV +PATH PYTHONPATH %{i}/lib/
## INITENV +PATH PYTHONPATH %{i}/lib/DBSAPI/
## INITENV SET DBS_CLIENT_CONFIG %{i}/lib/DBSAPI/dbs.config
## INITENV SET DBSCMD_HOME %{i}/lib/DBSAPI

Source: git://github.com/geneguvo/dbs2-client?obj=master/%realversion&export=%n&output=/%n.tar.gz

Requires: python openssl py2-zsi py2-pyxml

%prep
%setup -n %n
%build
%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d
cp -r Clients/Python/* %{i}/lib/
mv %{i}/lib/bin/* %{i}/bin/
python -m compileall %i/lib

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
