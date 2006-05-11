### RPM external xdaq 3.4
%define xdaqv %(echo %v |tr . _) 
%define libext so
# Download from cern afs area to speed up testing:
Source0: http://cmsdoc.cern.ch/Releases/XDAQ/XDAQ_%xdaqv/coretools_G_17559_V%xdaqv.tgz
Source1: http://cmsdoc.cern.ch/Releases/XDAQ/XDAQ_%xdaqv/powerpack_G_28175_V1_3_1.tgz
Source2: http://cmsdoc.cern.ch/Releases/XDAQ/XDAQ_%xdaqv/worksuite_G_28176_V1_4.tgz

%prep
%setup -T -b 0 -n TriDAS
%setup -D -T -b 1 -n TriDAS
%setup -D -T -b 2 -n TriDAS

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
# The following structure used as defined in Xdaq "simplify" script:
cd %{i}
mkdir -p %{i}/lib
mkdir -p %{i}/bin
# Catch-all 
find .  -type f ! -path "./lib/*.%{libext}" -name "*.%{libext}" -exec mv {}  %{i}/lib \;
find .  -type f ! -path "./bin/*.exe" -name "*.exe" -exec mv {} %{i}/bin \;

# Libraries from extern (not found cause they are symlinks)
cp -rdL daq/extern/*/linuxx86/lib/* %{i}/lib

find daq -type f ! -path "*/extern/*lib*" -name "*.a" -exec cp {} %{i}/lib \;
perl -p -i -e "s|^#!.*make|/usr/bin/env make|" %{i}/daq/extern/slp/openslp-1.2.0/debian/rules
