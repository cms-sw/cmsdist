### RPM external tkonlinesw 2.5.1

%define projectname trackerDAQ
%define releasename %{projectname}-%{realversion}
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)
Source: http://cern.ch/cms-sdt/source-mirrors/tkonlinesw/trackerDAQ-2.5.1-3.tgz
Patch0: tkonlinesw-2.5.1-gcc43
Patch1: tkonlinesw-2.5.1-TShare-64bit
Patch2: tkonlinesw-2.5.1-DbClient-64bit
Patch3: tkonlinesw-2.5.1-gcc44
Patch4: tkonlinesw-2.5.1-gcc43-2

# Note from Kristian: 
# xdaq dependency is here only to re-use its makefiles. 

Requires: oracle
%if "%online" != "true"
Requires: xerces-c
Requires: xdaq
Requires: systemtools
%else
Requires: onlinesystemtools
%endif

%prep
%setup -q -n %releasename
%patch0 -p1
case %cmsplatf in
  *amd64* ) 
%patch1 -p1
%patch2 -p1
  ;;
esac
%patch3 -p1
%patch4 -p1
# Clean up some mysterious old build within the sources that screws
# up the install by copying in an old libFed9UUtils.so 
# (this is really needed) 
rm -fR TrackerOnline/Fed9U/Fed9USoftware/Fed9UUtils/2.4/slc3_ia32_gcc323

case %gccver in
  4.*)
perl -p -i -e "s|-Werror||" FecSoftwareV3_0/generic/Makefile
  ;;
esac

%build
echo "pwd: $PWD"
# Set variables for requied externals to be picked up by configure:
################################################################################
# External Dependencies
################################################################################
export XDAQ_OS=linux
export XDAQ_PLATFORM=x86_slc4
export XERCESCROOT=${XERCES_C_ROOT}
export ENV_ORACLE_HOME=${ORACLE_ROOT}
export ENV_CMS_TK_ORACLE_HOME=${ENV_ORACLE_HOME}
# export TTCCIBUSADAPTER=CAENPCI # ?needed?

################################################################################
# Tracker Specific Definitions for compilation
################################################################################
export ENV_CMS_TK_BASE=%{_builddir}/%releasename
export ENV_CMS_TK_DIAG_ROOT=${ENV_CMS_TK_BASE}/DiagSystem
export ENV_CMS_TK_ONLINE_ROOT=${ENV_CMS_TK_BASE}/TrackerOnline/
export ENV_CMS_TK_COMMON=${ENV_CMS_TK_BASE}/TrackerOnline/2005/TrackerCommon/
export ENV_CMS_TK_XDAQ=${ENV_CMS_TK_BASE}/TrackerOnline/2005/TrackerXdaq/
export ENV_CMS_TK_APVE_ROOT=${ENV_CMS_TK_BASE}/TrackerOnline/APVe
export ENV_CMS_TK_FEC_ROOT=${ENV_CMS_TK_BASE}/FecSoftwareV3_0
export ENV_CMS_TK_FED9U_ROOT=${ENV_CMS_TK_BASE}/TrackerOnline/Fed9U/Fed9USoftware
export ENV_CMS_TK_ICUTILS=${ENV_CMS_TK_BASE}/TrackerOnline/2005/TrackerCommon//ICUtils
export ENV_CMS_TK_LASTGBOARD=${ENV_CMS_TK_BASE}/LAS
export ENV_CMS_TK_TTC_ROOT=${ENV_CMS_TK_BASE}/TTCSoftware # ?!?!
export ENV_CMS_TK_HAL_ROOT=${XDAQ_ROOT}

################################################################################
# Set these to NULL
################################################################################
export ROOTSYS=blah
export ENV_CMS_TK_CAEN_ROOT=blah
export ENV_CMS_TK_SBS_ROOT=blah

################################################################################
# Configure
################################################################################
case $(uname)-$(uname -p) in
  Linux-x86_64)
chmod +x ./configure && ./configure --with-xdaq-platform=x86_64
cd ${ENV_CMS_TK_FEC_ROOT} && chmod +x ./configure && ./configure --with-xdaq-platform=x86_64 && cd -
cd ${ENV_CMS_TK_FED9U_ROOT} && chmod +x ./configure && ./configure --with-xdaq-platform=x86_64 && cd -
  ;;
  * )
chmod +x ./configure && ./configure
cd ${ENV_CMS_TK_FEC_ROOT} && chmod +x ./configure && ./configure && cd -
cd ${ENV_CMS_TK_FED9U_ROOT} && chmod +x ./configure && ./configure && cd -
  ;;
esac

export CPPFLAGS=-fPIC
make cmssw
make cmsswinstall

%install
# Option --prefix in configure is not working yet, using tar:
tar -c -C  %{_builddir}/%{releasename}/opt/%{projectname} --exclude "libcppunit.so" include lib | tar -x -C %{i}
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=TkOnlineSw version=%v>
<info url="http://www.cern.ch/"></info>
<lib name=ICUtils>
<lib name=Fed9UUtils>
<Client>
 <Environment name=TKONLINESW_BASE default="%i"></Environment>
 <Environment name=LIBDIR value="$TKONLINESW_BASE/lib"></Environment>
 <Environment name=INCLUDE value="$TKONLINESW_BASE/include"></Environment>
</Client>
<use name=xerces-c>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/tkonlineswdb
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=TkOnlineSwDB version=%v>
<info url="http://www.cern.ch/"></info>
<lib name=ICUtils>
<lib name=Fed9UUtils>
<lib name=DeviceDescriptions>
<lib name=Fed9UDeviceFactory>
<Client>
 <Environment name=TKONLINESW_BASE default="%i"></Environment>
 <Environment name=LIBDIR value="$TKONLINESW_BASE/lib"></Environment>
 <Environment name=INCLUDE value="$TKONLINESW_BASE/include"></Environment>
</Client>
<use name=xerces-c>
<use name=oracle>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/scram.d/tkonlineswdb
