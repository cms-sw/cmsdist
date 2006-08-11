### RPM external xdaq 3.5
Requires: zlib
Requires: oracle
%define xdaqv %(echo %v |tr . _) 
%define libext so
%if "%cmsplatf" == "slc3_ia32_gcc323"
%define installDir linux/x86
%endif

# Download from cern afs area to speed up testing:
#Source0: http://cmsdoc.cern.ch/Releases/XDAQ/XDAQ_%xdaqv/coretools_G_17559_V%xdaqv.tgz
#Source1: http://cmsdoc.cern.ch/Releases/XDAQ/XDAQ_%xdaqv/powerpack_G_28175_V1_3_1.tgz
#Source2: http://cmsdoc.cern.ch/Releases/XDAQ/XDAQ_%xdaqv/worksuite_G_28176_V1_4.tgz
Source0: http://switch.dl.sourceforge.net/sourceforge/xdaq/coretools_G_17559_V%{xdaqv}.tgz
Source1: http://switch.dl.sourceforge.net/sourceforge/xdaq/powerpack_G_28175_V1_4.tgz
Source2: http://switch.dl.sourceforge.net/sourceforge/xdaq/worksuite_G_28176_V1_5.tgz

%prep
%setup -T -b 0 -n TriDAS
%setup -D -T -b 1 -n TriDAS
%setup -D -T -b 2 -n TriDAS
ls
perl -p -i -e "s|^#.*ksh(.*)|#!/usr/bin/env ksh $1|" daq/extern/SBSVME/1003/v2p3p0/sys/makefile \
                                                     daq/extern/SBSVME/1003/v2p3p0/sys/mkbtp
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
make Set=extern 
make Set=coretools
make Set=powerpack
make Set=worksuite
cd tstore
make  ORACLE_INCLUDE=$ORACLE_ROOT/include  ORACLE_LIB=$ORACLE_ROOT/lib
# The following structure used as defined in Xdaq "simplify" script:
#cd %{i}
# Catch-all
# cp -r ./lib %{i}/lib
# cp -r ./bin %{i}/bin
cd %{i}
find daq -path *src* -type d -exec rm -rf {} \;
# copies all the libraries in extern in %i/lib
mkdir -p %{i}/lib/linux/x86
mkdir -p %{i}/bin/linux/x86
(cd %{i}/lib; find ../daq -path "*/lib/lib*" -exec ln -s {} . \;)
(cd %{i}/lib/linux/x86; find ../../../daq -path "*/lib/lib*" -exec ln -s {} . \;)
(cd %{i}/bin; find ../daq -path "*/bin/*.exe" -exec ln -s {} . \;)
(cd %{i}/bin/linux/x86; find ../../../daq -path "*/bin/*.exe" -exec ln -s {} . \;)

#tar cpfv - `find daq -path "*/lib/*.%{libext}"` | ( cd  %{i}/lib; tar xpfv -)
#tar cpfv - `find daq -path "*/bin/*.exe" -type f` | ( cd  %{i}/bin; tar xpfv -)

#links them back to lib and bin
#find daq  -type f -name "*.%{libext}" -exec ln -sf {}  %{i}/lib \;
#find daq  -type f -name "*.%{libext}" -exec ln -sf ../../{} %{i}/lib/%installDir \;
#find daq  -type f -name "*.exe" -exec ln -sf {} %{i}/bin \; 
#find daq  -type f -name "*.exe" -exec ln -sf ../../{} %{i}/bin/%installDir \;

# Libraries from extern (not found cause they are symlinks)

#find daq -type f ! -path "*/extern/*lib*" -name "*.a" -exec cp {} %{i}/lib \;
perl -p -i -e "s|^#!.*make|#!/usr/bin/env make|" %{i}/daq/extern/slp/openslp-1.2.0/debian/rules
%post
find $RPM_INSTALL_PREFIX/%pkgrel -type l | xargs ls -la | sed -e "s|.*[ ]\(/.*\) -> \(.*\)| \2 \1|;s|[ ]/[^ ]*/external| $RPM_INSTALL_PREFIX/%cmsplatf/external|g"
find $RPM_INSTALL_PREFIX/%pkgrel -type l | xargs ls -la | sed -e "s|.*[ ]\(/.*\) -> \(.*\)| \2 \1|;s|[ ]/[^ ]*/external| $RPM_INSTALL_PREFIX/%cmsplatf/external|g" | xargs -n2 ln -sf
