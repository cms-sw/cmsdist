### RPM external xdaq 3.9.0-CMS3
Requires: zlib mimetic xerces-c uuid
%define xdaqv %(echo %v | cut -f1 -d- | tr . _) 
%define libext so
%if "%cmsplatf" == "slc3_ia32_gcc323"
%define installDir linux/x86
%endif

# Download from cern afs area to speed up testing:
Source0: http://switch.dl.sourceforge.net/sourceforge/xdaq/coretools_G_V%{xdaqv}.tgz
Source1: http://switch.dl.sourceforge.net/sourceforge/xdaq/powerpack_G_V1_9_0.tgz
Source2: http://switch.dl.sourceforge.net/sourceforge/xdaq/worksuite_G_V1_8_0.tgz
Patch: xdaq_39_oracle
Patch1: xdaq-3.9.0-uuid
Patch2: xdaq-3.9.0-nossh

%prep
%setup -T -b 0 -n TriDAS
%setup -D -T -b 1 -n TriDAS
%setup -D -T -b 2 -n TriDAS

#%patch0 -p2
%patch1 -p1
%patch2 -p1
ls
#perl -p -i -e "s|^#.*ksh(.*)|#!/usr/bin/env ksh $1|" daq/extern/SBSVME/1003/v2p3p0/sys/makefile \
#                                                     daq/extern/SBSVME/1003/v2p3p0/sys/mkbtp
echo " Install root in prep:" %{i}    %{pkginstroot}

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
 
make CPPDEFINES=linux Set=extern_coretools install
make CPPDEFINES=linux Set=coretools install
make CPPDEFINES=linux Set=extern_powerpack install
make CPPDEFINES=linux Set=powerpack install
cd xdaq2rc
make CPPDEFINES=linux install
cd ..


# The following structure used as defined in Xdaq "simplify" script:
cd %{i}
mv x86*/lib .
mv x86*/bin .
mv x86*/include .
mkdir include/interface
mv daq/interface/evb/include/interface/evb include/interface
mv daq/interface/shared/include/interface/shared include/interface

rm -fr daq 
rm -fr CVS
rm -fr x86*

# Libraries from extern (not found cause they are symlinks)

#find daq -type f ! -path "*/extern/*lib*" -name "*.a" -exec cp {} %{i}/lib \;
perl -p -i -e "s|^#!.*make|#!/usr/bin/env make|" %{i}/daq/extern/slp/openslp-1.2.0/debian/rules
%post
find $RPM_INSTALL_PREFIX/%pkgrel -type l | xargs ls -la | sed -e "s|.*[ ]\(/.*\) -> \(.*\)| \2 \1|;s|[ ]/[^ ]*/external| $RPM_INSTALL_PREFIX/%cmsplatf/external|g" | xargs -n2 ln -sf
