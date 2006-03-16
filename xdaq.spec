### RPM external xdaq 3.4
%define xdaqv %(echo %v |tr . _) 
# Download from cern afs area to speed up testing:
Source: http://cmsdoc.cern.ch/Releases/XDAQ/XDAQ_%xdaqv/coretools_G_17559_V%xdaqv.tgz

%prep
%setup -n TriDAS
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
# The following structure used as defined in Xdaq "simplify" script:
cd %{i}
mkdir -p %{i}/lib/linux/x86
mkdir -p %{i}/bin/linux/x86
# Catch-all 
find .  -type f ! -path "./lib/*.so" -name "*.so" -exec mv {}  lib/linux/x86 \;
find .  -type f ! -path "./bin/*.exe" -name "*.exe" -exec mv {} bin/linux/x86 \;

# Libraries from extern (not found cause they are symlinks)
cp -d daq/extern/*/linuxx86/lib/* lib/linux/x86
