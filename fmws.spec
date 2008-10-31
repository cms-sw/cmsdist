### RPM cms fmws 0.1.7_pre1
## INITENV +PATH PYTHONPATH %i/lib/
## INITENV SET FMWSHOME $FMWS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV SET PYTHONPATH ${FMWSHOME}:${PYTHONPATH}

####%define cvstag %{realversion}
%define moduleName FILEMOVER
%define exportName FILEMOVER
%define cvstag V01_00_01
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
####Source: http://t2.unl.edu/store/CmsFileServer-%{realversion}.tar.gz
Source: %cvsserver&strategy=checkout&module=COMP/%{moduleName}&nocache=true&export=%{exportName}&tag=-r%{cvstag}&output=/%{moduleName}.tar.gz
Requires: python openssl cherrypy py2-cheetah webtools yui java-jdk srmcp elementtree

%prep
%setup -n %{moduleName}
%build

%install
mkdir -p %{i}/bin
mkdir -p %{i}/lib
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/etc/init.d
pyver=`echo $PYTHON_VERSION | cut -d. -f1,2`
mkdir -p %i/lib/python$pyver/site-packages
cp -r src/CmsFileServer/* %i/lib/python$pyver/site-packages
cp    etc/fmws_init %{i}/etc/init.d
chmod a+x %{i}/etc/init.d/*

(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.sh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.sh"; \
 echo "source $CHERRYPY_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_CHEETAH_ROOT/etc/profile.d/init.sh"; \
 echo "source $YUI_ROOT/etc/profile.d/init.sh"; \
 echo "source $SRMCP_ROOT/etc/profile.d/init.sh"; \
 echo "source $ELEMENTTREE_ROOT/etc/profile.d/init.sh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.sh"; \
 echo "export JAVA_HOME=$JAVA_JDK_ROOT"
 echo "export LD_LIBRARY_PATH=\$SRMCP_ROOT/bin:\$LD_LIBRARY_PATH"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.csh"; \
 echo "source $CHERRYPY_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_CHEETAH_ROOT/etc/profile.d/init.csh"; \
 echo "source $YUI_ROOT/etc/profile.d/init.csh"; \
 echo "source $SRMCP_ROOT/etc/profile.d/init.csh"; \
 echo "source $ELEMENTTREE_ROOT/etc/profile.d/init.csh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.csh"; \
 echo "setenv JAVA_HOME $JAVA_JDK_ROOT"
 echo "setenv LD_LIBRARY_PATH \$SRMCP_ROOT/bin:\$LD_LIBRARY_PATH"; \
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

. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
mkdir -p $FMWSHOME/{logs,css}
if [ -d /data/download ]; then
   ln -s /data/download $FMWSHOME/download
else
   mkdir -p $FMWSHOME/download
fi
cat > $FMWSHOME/FMWS.conf << END
#
# Location for log files
#
LOGGERDIR=$FMWSHOME/logs
#
# Location of loca file storage
#
TRANSFERDIR=/data/pool
#
# Verbosity level for the FMWS server
#
VERBOSELEVEL=1
#
# Number of files allowed to users for simultaneous download
#
MAXTRANSFER=3
#
#
# Number of query/per user/per day
#
USERTRANSFERPERDAY=10
#
END
