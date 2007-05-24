### RPM external tkonlinesw 0.3
%define projectname trackerDAQ
%define releasename %{projectname}-%{v}
Source: http://cmsdoc.cern.ch/cms/cmt/online/rpm/SOURCE/%{releasename}.tgz
Patch: Fed9U-gcc3.4
Requires: xerces-c
Requires: xdaq
Requires: oracle

%prep
%setup -q -n %releasename
%patch -p1

# This is a kludge around a kludge...
%if "%cmsplatf" == "slc4_amd64_gcc345"
tar xzvf %_sourcedir/%{n}-%{v}.slc4_ia32_gcc345.tar.gz
%endif

%build
echo "pwd: $PWD"
# Set variables for requied externals to be picked up by configure:
export XERCESCROOT=${XERCES_C_ROOT}
export XDAQ_ROOT=${XDAQ_ROOT}
export ENV_ORACLE_HOME=${ORACLE_ROOT}

export ENV_CMS_TK_BASE=%{_builddir}/%releasename
export ENV_CMS_TK_DIAG_ROOT=${ENV_CMS_TK_BASE}/DiagSystem
export ENV_CMS_TK_ONLINE_ROOT=${ENV_CMS_TK_BASE}/TrackerOnline/
export ENV_CMS_TK_COMMON=${ENV_CMS_TK_BASE}/TrackerOnline/2005/TrackerCommon/
export ENV_CMS_TK_XDAQ=${ENV_CMS_TK_BASE}/TrackerOnline/2005/TrackerXdaq/
export ENV_CMS_TK_APVE_ROOT=${ENV_CMS_TK_BASE}/TrackerOnline/APVe
export APVE_ROOT=${ENV_CMS_TK_APVE_ROOT}
export ENV_CMS_TK_FEC_ROOT=${ENV_CMS_TK_BASE}/FecSoftwareV3_0
export ENV_CMS_TK_FED9U_ROOT=${ENV_CMS_TK_BASE}/TrackerOnline/Fed9U/Fed9USoftware
export ENV_CMS_TK_ICUTILS=${ENV_CMS_TK_COMMON}/ICUtils
export ENV_CMS_TK_LASTGBOARD=${ENV_CMS_TK_BASE}/LAS
export ENV_CMS_TK_TTC_ROOT=${ENV_CMS_TK_BASE}/TTCSoftware

# set these to NULL
export ROOTSYS=blah
export ENV_CMS_TK_CAEN_ROOT=blah
export ENV_CMS_TK_SBS_ROOT=blah

cd ${ENV_CMS_TK_FEC_ROOT} && chmod +x ./configure  && ./configure && cd -
cd ${ENV_CMS_TK_FED9U_ROOT} && chmod +x ./configure  && ./configure && cd -

# order matters ...
cd ${ENV_CMS_TK_ICUTILS} && make && cd -
cd ${ENV_CMS_TK_FED9U_ROOT} && make Fed9UUtils && cd -
cd ${ENV_CMS_TK_FED9U_ROOT} && make Fed9UDeviceFactory && cd -
cd ${ENV_CMS_TK_FEC_ROOT} && make DeviceFactory && cd -
make install

%install
# Option --prefix in configure is not working yet, using tar:
tar -c -C  %{_builddir}/%{releasename}/opt/%{projectname} --exclude "libcppunit.so" include lib | tar -x -C %{i}
