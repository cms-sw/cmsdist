### RPM external millepede 2.0
# CAREFUL: NO VERSION IN TARBALL !!!
# Source: http://www.desy.de/~blobel/Mptwo.tgz
Source: http://cmsrep.cern.ch/cmssw/millepede-mirror/millepede-2.0.tar.gz

Patch: millepede-may2007

%prep
%setup -n millepede-%realversion
%patch -p1

%build
make %makeprocesses

%install
# make install

# Toolfile with only PATH

%post


