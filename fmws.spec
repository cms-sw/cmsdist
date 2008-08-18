### RPM cms fmws 0_1_1
## INITENV +PATH PYTHONPATH %i/lib/
## INITENV +PATH PYTHONPATH %i/lib/src
## INITENV +PATH PYTHONPATH %i/lib/src/CmsFileServer

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
#Source: %cvsserver&strategy=checkout&module=DBS/Clients/Python&nocache=true&export=DBS&tag=-r%{cvstag}&output=/fmws.tar.gz
#Source: svn://root.cern.ch/svn/root/trunk?scheme=https&module=root&output=/root.tgz
#Source: svn://t2.unl.edu/brian?scheme=http&module=CmsFileServer&output=/fmws.tar.gz
Source: http://t2.unl.edu/store/CmsFileServer-0.1.1.tar.gz
Requires: python openssl cherrypy py2-cheetah webtools yui java-jdk srmcp

%prep
%build

%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/etc/init.d
cp -r src %{i}/lib/
cp -r src/CmsFileServer/fmws_init %{i}/etc/init.d
chmod a+x %{i}/etc/init.d/*

(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.sh"; \
 echo "export LD_LIBRARY_PATH=\$SRM_PATH/bin:\$LD_LIBRARY_PATH"; \
 echo "export FMWSHOME=\$FMWS_ROOT/lib"; \
 echo "export FMWSTRANSFERDIR=/data/filemover/download"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo "setenv LD_LIBRARY_PATH \$SRM_PATH/bin:\$LD_LIBRARY_PATH"; \
 echo "setenv FMWSHOME \$FMWS_ROOT/lib"; \
 echo "setenv FMWSTRANSFERDIR /data/filemover/download"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=dbs-client version=%v>
<client>
 <Environment name=FMWS_BASE default="%i"></Environment>
</client>
<Runtime name=PATH value="$FMWS_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}etc/scram.d/%n

