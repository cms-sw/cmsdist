### RPM external xdaq VR16021
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Requires: zlib mimetic xerces-c uuid sqlite
%define xdaqv %(echo %v | cut -f1 -d- | tr . _) 
%define libext so
%define svntrunk  %(echo %v | sed 's|^VR||')
Source: svn://svn.cern.ch/reps/cmsos/releases/baseline10/tags/base/?scheme=svn+ssh&revision=%svntrunk&strategy=export&module=xdaq&output=/xdaq.tar.gz

Patch0: xdaq_VR16021_build
Patch1: xdaq_mfDefs_flags
Patch2: xdaq_VR15544_gcc44
Patch3: xdaq-VR16021-gcc45

Provides: /bin/awk

%prep
%setup -T -b 0 -n xdaq

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# Xdaq does not provide makeinstall,  it uses "simplify" script instead to 
# reorganize the directory structure after the build is done.
# Therefore build is done in the install area.

%install
# Copy all code into the installation area, and build directly there:
cp -rp *  %{i} # assuming there are no symlinks in the original source code
cd %{i}
export XDAQ_ROOT=$PWD
cd %{i}/daq

export MIMETIC_PREFIX=$MIMETIC_ROOT
export XERCES_PREFIX=$XERCES_C_ROOT
export UUID_LIB_PREFIX=$UUID_ROOT/lib
export SQLITE_PREFIX=$SQLITE_ROOT
export SEARCH_PATH=$PATH

make CPPDEFINES=linux Set=extern_coretools install
make CPPDEFINES=linux Set=coretools install
make CPPDEFINES=linux Set=extern_powerpack install
make CPPDEFINES=linux Set=powerpack install
make CPPDEFINES=linux Set=general_worksuite install

# The following structure used as defined in Xdaq "simplify" script:
cd %{i}
mv x86*/lib .
mv x86*/bin .
mv x86*/include .
# Make the following directory (it will be missing in the gcc4 case where
# things fail during the build and scram at least needs to see it)
mkdir -p include/linux

mkdir -p htdocs

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

