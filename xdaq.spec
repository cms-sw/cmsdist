### RPM external xdaq VR16021

Requires: zlib mimetic xerces-c uuid sqlite
%define xdaqv %(echo %v | cut -f1 -d- | tr . _) 
%define libext so
%define svntrunk  %(echo %v | sed 's|^VR||')
Source: svn://svn.cern.ch/reps/cmsos/releases/baseline10/tags/base/?scheme=svn+ssh&revision=%svntrunk&strategy=export&module=xdaq&output=/xdaq.tar.gz

Patch0: xdaq_VR16021_build
Patch1: xdaq_mfDefs_flags
Patch2: xdaq_VR15544_gcc44
Patch3: xdaq-VR16021-gcc45
Patch4: xdaq-VR16021-macosx

Provides: /bin/awk

%prep
%setup -T -b 0 -n xdaq

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# We do not apply the macosx patch on linux, because we
# do not want to have to validate it.
case %cmsos in
  osx*)
%patch4 -p1
  mkdir daq/toolbox/include/macosx-new
  mv daq/toolbox/include/macosx daq/toolbox/include/macosx-new/toolbox
  mv daq/toolbox/include/macosx-new daq/toolbox/include/macosx
  # i2o package is case sensitive, but it looks like the all upper case 
  # (or partially upper case) files are from an ancient version while the 
  # lowercase one are the one needed, therefore we extract by hand the required
  # files.
  cd ..
    rm -f xdaq/daq/extern/i2o/include/i2o/shared/i2omsg.h
    rm -f xdaq/daq/extern/i2o/include/i2o/shared/i2oexec.h
    rm -f xdaq/daq/extern/i2o/include/i2o/shared/I2OTYPES.h
    rm -f xdaq/daq/extern/i2o/include/i2o/shared/I2omodule.h
    rm -f xdaq/daq/extern/i2o/include/i2o/shared/I2outil.h
    tar xzvf %{_sourcedir}/xdaq.tar.gz xdaq/daq/extern/i2o/include/i2o/shared/i2omsg.h \
                                       xdaq/daq/extern/i2o/include/i2o/shared/i2oexec.h \
                                       xdaq/daq/extern/i2o/include/i2o/shared/i2otypes.h \
                                       xdaq/daq/extern/i2o/include/i2o/shared/i2omodule.h \
                                       xdaq/daq/extern/i2o/include/i2o/shared/i2outil.h
  cd xdaq 
;;
esac

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
  osx*) 
	PLATF_DEFINE=macosx 
	# Hack to make sure things compile on the mac.
	find . -name Makefile.rules -exec perl -p -i -e 's|cp -pd|cp -p|g' {} \;
	;;
  slc*) PLATF_DEFINE=linux ;;
esac

case %cmsplatf in
  slc*)
    make CPPDEFINES=$PLATF_DEFINE Set=extern_coretools install
    make CPPDEFINES=$PLATF_DEFINE Set=coretools install
    make CPPDEFINES=$PLATF_DEFINE Set=extern_powerpack install
    make CPPDEFINES=$PLATF_DEFINE Set=powerpack install
    make CPPDEFINES=$PLATF_DEFINE Set=general_worksuite install
  ;;
  osx*)
    make -k CPPDEFINES=$PLATF_DEFINE CCDefines='-DHAVE_SOCKADDR_STORAGE_SS_LEN=linux -DLIBRARY_PATH_VARIABLE=\"DYLD_LIBRARY_PATH\" -DRLIMIT_SIGPENDING=-1 -DRLIMIT_LOCKS=-1 -DRLIMIT_MSGQUEUE=-1 -DRLIMIT_SIGPENDING=-1 -DLITTLE_ENDIAN__ -D"xdr_uint8_t(x,y)=false" -D"xdr_int8_t(x,y)=false" -D"xdr_uint16_t(x,y)=false" -D"xdr_uint32_t(x,y)=false" -D"xdr_uint64_t(x,y)=false"' Set=extern_coretools install || true
    make -k CPPDEFINES=$PLATF_DEFINE CCDefines='-DHAVE_SOCKADDR_STORAGE_SS_LEN=linux -DLIBRARY_PATH_VARIABLE=\"DYLD_LIBRARY_PATH\" -DRLIMIT_SIGPENDING=-1 -DRLIMIT_LOCKS=-1 -DRLIMIT_MSGQUEUE=-1 -DRLIMIT_SIGPENDING=-1 -DLITTLE_ENDIAN__ -D"xdr_uint8_t(x,y)=false" -D"xdr_int8_t(x,y)=false" -D"xdr_uint16_t(x,y)=false" -D"xdr_uint32_t(x,y)=false" -D"xdr_uint64_t(x,y)=false"' Set=coretools install || true
    make -k CPPDEFINES=$PLATF_DEFINE CCDefines='-DHAVE_SOCKADDR_STORAGE_SS_LEN=linux -DLIBRARY_PATH_VARIABLE=\"DYLD_LIBRARY_PATH\" -DRLIMIT_SIGPENDING=-1 -DRLIMIT_LOCKS=-1 -DRLIMIT_MSGQUEUE=-1 -DRLIMIT_SIGPENDING=-1 -DLITTLE_ENDIAN__ -D"xdr_uint8_t(x,y)=false" -D"xdr_int8_t(x,y)=false" -D"xdr_uint16_t(x,y)=false" -D"xdr_uint32_t(x,y)=false" -D"xdr_uint64_t(x,y)=false"' Set=extern_powerpack install || true
    make -k CPPDEFINES=$PLATF_DEFINE CCDefines='-DHAVE_SOCKADDR_STORAGE_SS_LEN=linux -DLIBRARY_PATH_VARIABLE=\"DYLD_LIBRARY_PATH\" -DRLIMIT_SIGPENDING=-1 -DRLIMIT_LOCKS=-1 -DRLIMIT_MSGQUEUE=-1 -DRLIMIT_SIGPENDING=-1 -DLITTLE_ENDIAN__ -D"xdr_uint8_t(x,y)=false" -D"xdr_int8_t(x,y)=false" -D"xdr_uint16_t(x,y)=false" -D"xdr_uint32_t(x,y)=false" -D"xdr_uint64_t(x,y)=false"' Set=powerpack install || true
    make -k CPPDEFINES=$PLATF_DEFINE CCDefines='-DHAVE_SOCKADDR_STORAGE_SS_LEN=linux -DLIBRARY_PATH_VARIABLE=\"DYLD_LIBRARY_PATH\" -DRLIMIT_SIGPENDING=-1 -DRLIMIT_LOCKS=-1 -DRLIMIT_MSGQUEUE=-1 -DRLIMIT_SIGPENDING=-1 -DLITTLE_ENDIAN__ -D"xdr_uint8_t(x,y)=false" -D"xdr_int8_t(x,y)=false" -D"xdr_uint16_t(x,y)=false" -D"xdr_uint32_t(x,y)=false" -D"xdr_uint64_t(x,y)=false"' Set=general_worksuite install || true
  ;;
esac

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

