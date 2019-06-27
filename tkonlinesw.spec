### RPM external tkonlinesw 4.2.0-1_gcc7
%define projectname trackerDAQ
%define releasename %{projectname}-4.2-tkonline
Source0: http://cms-trackerdaq-service.web.cern.ch/cms-trackerdaq-service/download/sources/trackerDAQ-%{realversion}.tgz
Patch0: tkonlinesw-2.7.0-macosx
Patch1: tkonlinesw-4.0-clang-hash_map

# NOTE: given how broken the standard build system is
#       on macosx, it's not worth fixing it.
#       The 4 libraries we need can be built with the
#       attached 118 lines of cmakefile, at least on macosx 
#       (and without dependencies on xdaq).
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Source1: tkonlinesw-cmake-build
Requires: cmake
%endif

Requires: oracle
Requires: xerces-c
Requires: gmake
Requires: systemtools
Requires: root

%prep
%setup -q -n %releasename
%patch1 -p1
case %cmsos in 
  osx*)
%patch0 -p1
  ;;
esac
# Clean up some mysterious old build within the sources that screws
# up the install by copying in an old libFed9UUtils.so 
# (this is really needed) 
rm -fR TrackerOnline/Fed9U/Fed9USoftware/Fed9UUtils/2.4/slc3_ia32_gcc323

perl -p -i -e "s|-Werror||" FecSoftwareV3_0/generic/Makefile


%build
###############################################################################
# Tracker Specific Definitions for running, should just be this ...
################################################################################
export ENV_TRACKER_DAQ=%{_builddir}/%releasename/opt/trackerDAQ

################################################################################
# Tracker Specific Definitions for compilation
################################################################################
export XDAQ_ROOT=$PWD/FecSoftwareV3_0/generic
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
    export XDAQ_PLATFORM=x86_slc4
  ;;
esac

export ENV_CMS_TK_ORACLE_HOME=${ORACLE_ROOT}
export ENV_ORACLE_HOME=${ORACLE_ROOT}
export XERCESCROOT=${XERCES_C_ROOT}
export XDAQ_ROOT

################################################################################
# Configure
################################################################################
case %cmsos in
  slc*)
    chmod +x ./configure && ./configure --with-xdaq-platform=x86_64
    cd ${ENV_CMS_TK_FEC_ROOT} && chmod +x ./configure && ./configure --with-xdaq-platform=x86_64 && cd -
    cd ${ENV_CMS_TK_FED9U_ROOT} && chmod +x ./configure && ./configure --with-xdaq-platform=x86_64 && cd -
  ;;
  osx*)
    chmod +x ./configure && ./configure
    cd ${ENV_CMS_TK_FEC_ROOT} && chmod +x ./configure && ./configure && cd -
    cd ${ENV_CMS_TK_FED9U_ROOT} && chmod +x ./configure && ./configure && cd -
  ;;
esac

# The CPPFLAGS is probably not needed. Clean up at some point.
export CPPFLAGS="-fPIC"
export CFLAGS="-O2 -fPIC"
export CXXFLAGS="-O2 -fPIC"
case %cmsos in 
  slc*)
    make cmssw
    make cmsswinstall
  ;;
  osx*)
    # We still need the old makefile to generate a few headers.
    make -C TrackerOnline/Fed9U/Fed9USoftware/Fed9UUtils include/Fed9UUtils.hh
    make -C TrackerOnline/Fed9U/Fed9USoftware Fed9UUtils/include/Fed9UVersion.inc

    # We use CMake for all the rest since the build system on macosx
    # is simply broken by circular dependencies and other linux only bits.
    cp %_sourcedir/tkonlinesw-cmake-build ./CMakeLists.txt
    make -C TrackerOnline/Fed9U/Fed9USoftware/Fed9UUtils include/Fed9UUtils.hh
    cmake . -DORACLE_ROOT=${ORACLE_ROOT} \
	    -DCMAKE_C_COMPILER="`which gcc`" \
	    -DCMAKE_CXX_COMPILER="`which c++`" \
	    -DCMAKE_LINKER=`which ld` \
	    -DXERCES_ROOT=${XERCES_C_ROOT} \
	    -DXERCESC=2 -DCMAKE_INSTALL_PREFIX=%i
    make %makeprocesses
    make install
  ;;
esac

%install
# Again, installing is actually done by make install on macosx.
case %cmsos in
  slc*)
    # Option --prefix in configure is not working yet, using tar:
    tar -c -C  %{_builddir}/%{releasename}/opt/%{projectname} include lib | tar -x -C %{i}
  ;;
esac
# bla bla
