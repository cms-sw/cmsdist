### RPM external xdaq VR17173

%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
Requires: zlib mimetic xerces-c sqlite
%if "%online" != "true"
Requires: uuid
%else
Requires: onlinesystemtools
%endif

%define xdaqv %(echo %v | cut -f1 -d- | tr . _) 
%define libext so
%define svntrunk  %(echo %v | sed 's|^VR||')
Source: svn://svnweb.cern.ch/guest/cmsos/releases/baseline11/trunk/?scheme=http&revision=%svntrunk&strategy=export&module=xdaq&output=/xdaq.tar.gz

Patch0: xdaq_VR16993_build
Patch1: xdaq_mfDefs_flags
Patch2: xdaq-VR16796-gcc46
Patch3: xdaq-VR17173-macosx
Patch4: xdaq-VR17173-gcc46
#Patch5: xdaq-VR17173-remove-sqlite-macosx
Patch6: xdaq-VR17173-xalan-remove-hardcoded-lib-paths-linux-macosx
Patch7: xdaq-VR17173-remove-stropts
Patch8: xdaq-VR17173-fix-gcc47-cxx11
Patch9: xdaq-VR17173-drop-cgicc-docs

Provides: /bin/awk
# This is needed on macosx because this is the install_name for the .so
# library.  We could simply run install_name_tool, but I'm not sure if somthing
# will break elsewhere.
Provides: libasyncresolv.0

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -T -b 0 -n xdaq

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#patch5 -p0
%patch6 -p0
%patch7 -p1
%patch8 -p1
%patch9 -p2

%build
# Xdaq does not provide makeinstall,  it uses "simplify" script instead to 
# reorganize the directory structure after the build is done.
# Therefore build is done in the install area.

%install
# Copy all code into the installation area, and build directly there:
rm -rf %i
mkdir -p %i
cp -rp *  %{i} # assuming there are no symlinks in the original source code
cd %{i}
export XDAQ_ROOT=$PWD
cd %{i}/daq

export MIMETIC_PREFIX=$MIMETIC_ROOT
export XERCES_PREFIX=$XERCES_C_ROOT
export UUID_LIB_PREFIX=$UUID_ROOT/lib
export SQLITE_PREFIX=$SQLITE_ROOT
export SEARCH_PATH=$PATH

case %cmsplatf in
  osx*) PLATF_DEFINE=macosx ;;
  slc*) PLATF_DEFINE=linux ;;
esac

export CXX="%cms_cxx"
export CXXFLAGS="%cms_cxxflags"
export UserCCFlags="%cms_cxxflags"
if [ $(uname) != Darwin ]; then
  # Changes for Linux
  sed -ibak "s/\(^CXX.*= \)\(.*\)/\1%cms_cxx/g" ../config/mfDefs.linux
  sed -ibak "s/\(^CFlags.*= \)\(.*\)/\1-O2 -fPIC/g" ../config/mfDefs.linux
  sed -ibak "s/\(^CCFlags.*= \)\(.*\)/\1-Wall -fPIC %cms_cxxflags/g" ../config/mfDefs.linux
else
  # Changes for Darwin
  sed -ibak "s/\(^CXX.*= \)\(.*\)/\1%cms_cxx/g" ../config/mfDefs.macosx
  sed -ibak "s/\(^CFlags.*= \)\(.*\)/\1/g" ../config/mfDefs.macosx
  sed -ibak "s/\(^CCFlags.*= \)\(.*\)/\1%cms_cxxflags/g" ../config/mfDefs.macosx
fi

make CPPDEFINES=$PLATF_DEFINE Set=extern_coretools install
make CPPDEFINES=$PLATF_DEFINE Set=coretools install
make CPPDEFINES=$PLATF_DEFINE Set=extern_powerpack install
make CPPDEFINES=$PLATF_DEFINE Set=powerpack install
make CPPDEFINES=$PLATF_DEFINE Set=general_worksuite install

# The following structure used as defined in Xdaq "simplify" script:
cd %{i}
mv x86*/lib .
mv x86*/bin .
mv x86*/include .
# Make the following directory (it will be missing in the gcc4 case where
# things fail during the build and scram at least needs to see it)
mkdir -p include/linux
mkdir -p include/macosx
mkdir -p htdocs

case %cmsplatf in 
  slc*)
    for subdir in `echo "xdaq2rc"; grep -h -v \# config/mfSet.coretools config/mfSet.extern_coretools config/mfSet.extern_powerpack config/mfSet.powerpack | grep -v Packages= | grep '[a-z]' | awk '{print $1}'`
    do
      mkdir -p %{i}/htdocs/$subdir/{images,xml,html}
      echo $subdir
      if [ -d daq/$subdir/xml ]; then
	    cd daq/$subdir/xml
        find . -name "*.*" -exec install -m 655 -D {} %{i}/htdocs/$subdir/xml/{} \;
	    cd %{i}
      fi	
	  if [ -d daq/$subdir/images ]; then
	    cd daq/$subdir/images
        find . -name "*.*" -exec install -m 655 -D {} %{i}/htdocs/$subdir/images/{} \;
		cd %{i}
      fi	
      if [ -d daq/$subdir/html ]; then
	    cd daq/$subdir/html
        find . -name "*.*" -exec install -m 655 -D {} %{i}/htdocs/$subdir/html/{} \;
	    cd %{i}
      fi
    done
  ;;
esac

mkdir -p include/interface
mv daq/interface/evb/include/interface/evb include/interface
mv daq/interface/shared/include/interface/shared include/interface
mkdir -p etc
mv daq/xdaq/etc/default.profile etc/
rm -fr daq
rm -fr CVS
rm -fr x86*
rm -fR java
rm -fR htdocs
ln -s libasyncresolv %{i}/lib/libasyncresolv.so
rm -f %{i}/lib/lib*.a %{i}/lib/lib*.la

# Libraries from extern (not found cause they are symlinks)

#find daq -type f ! -path "*/extern/*lib*" -name "*.a" -exec cp {} %{i}/lib \;
perl -p -i -e "s|^#!.*make|#!/usr/bin/env make|" %{i}/daq/extern/slp/openslp-1.2.0/debian/rules
