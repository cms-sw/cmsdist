### RPM external tkonlinesw 2.7.0

%define projectname trackerDAQ
%define releasename %{projectname}-%{realversion}
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)
Source: http://cms-trackerdaq-service.web.cern.ch/cms-trackerdaq-service/download/sources/trackerDAQ-2.7.0-9.tgz
Patch0: tkonlinesw-2.7.0-macosx

# Note from Kristian: 
# xdaq dependency is here only to re-use its makefiles. 

Requires: oracle
%if "%online" != "true"
Requires: xerces-c
Requires: xdaq
Requires: systemtools
Requires: gmake
%else
Requires: onlinesystemtools
%endif

%prep
%setup -q -n %releasename
case %cmsos in 
  osx*)
%patch0 -p1
  ;;
esac
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

###############################################################################
# Tracker Specific Definitions for running, should just be this ...
################################################################################
export ENV_TRACKER_DAQ=%{_builddir}/%releasename/opt/trackerDAQ

################################################################################
# Tracker Specific Definitions for compilation
################################################################################
export XDAQ_RPMBUILD=yes
export USBFEC=no
export PCIFEC=yes
export ENV_CMS_TK_BASE=%{_builddir}/%releasename
export ENV_CMS_TK_DIAG_ROOT=%{_builddir}/%releasename/DiagSystem
export ENV_CMS_TK_ONLINE_ROOT=%{_builddir}/%releasename/TrackerOnline/
export ENV_CMS_TK_COMMON=%{_builddir}/%releasename/TrackerOnline/2005/TrackerCommon/
export ENV_CMS_TK_XDAQ=%{_builddir}/%releasename/TrackerOnline/2005/TrackerXdaq/
export ENV_CMS_TK_APVE_ROOT=%{_builddir}/%releasename/TrackerOnline/APVe
export ENV_CMS_TK_FEC_ROOT=%{_builddir}/%releasename/FecSoftwareV3_0
export ENV_CMS_TK_FED9U_ROOT=%{_builddir}/%releasename/TrackerOnline/Fed9U/Fed9USoftware
export ENV_CMS_TK_ICUTILS=%{_builddir}/%releasename/TrackerOnline/2005/TrackerCommon//ICUtils
export ENV_CMS_TK_LASTGBOARD=%{_builddir}/%releasename/LAS

################################################################################
# Fake variables for the configure script only
################################################################################
# We use an empty directory because the path neeeds to exist.
mkdir -p %i/dummy/Linux/lib
export ENV_CMS_TK_HAL_ROOT=%{i}/dummy/Linux
export ROOTSYS=%{i}/dummy/Linux
export ENV_CMS_TK_CAEN_ROOT=%{i}/dummy/Linux
export ENV_CMS_TK_SBS_ROOT=%{i}/dummy/Linux
export ENV_CMS_TK_TTC_ROOT=%{i}/dummy/Linux

################################################################################
# External Dependencies
################################################################################
case %cmsos in 
  slc*)
    export XDAQ_OS=linux
    export XDAQ_PLATFORM=x86_slc4
  ;;
  osx*)
    export XDAQ_OS=macosx
    export XDAQ_PLATFORM=x86_
    export ENV_CMS_TK_FED9U_ORACLE_LIBRARY="-locci -lclntsh -lnnz10"
  ;;
esac

export ENV_CMS_TK_ORACLE_HOME=${ORACLE_ROOT}
export ENV_ORACLE_HOME=${ORACLE_ROOT}
export XERCESCROOT=${XERCES_C_ROOT}
export XDAQ_ROOT

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
# On osx ignore build errors and build as much as you possibly can.
# FIXME: looks like there are some undefined symbols which on mac are
#        fatal.
case %cmsos in 
  slc*)
    make cmssw
    make cmsswinstall
  ;;
  osx*)
    make -k cmssw || true
    make -k cmsswinstall || true
  ;;
esac

%install
# Option --prefix in configure is not working yet, using tar:
tar -c -C  %{_builddir}/%{releasename}/opt/%{projectname} --exclude "libcppunit.so" include lib | tar -x -C %{i}
