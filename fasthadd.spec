### RPM external fasthadd 1.1

#Change the commit hash every time a new version is needed.
#Commit mapped to CMSSW_7_1_6
%define commit e193ee35083c2c1583e186130891087d6a4c7ac1
Source0: https://raw.githubusercontent.com/cms-sw/cmssw/%commit/DQMServices/Components/bin/fastHadd.cc
Source1: https://raw.githubusercontent.com/cms-sw/cmssw/%commit/DQMServices/Core/src/ROOTFilePB.proto
Requires: protobuf root

%prep

%build
mkdir -p %i/bin %i/etc/profile.d

cp %{_sourcedir}/fastHadd.cc .
cp %{_sourcedir}/ROOTFilePB.proto .
protoc -I ./ --cpp_out=./ ROOTFilePB.proto
perl -p -i -e 's|DQMServices/Core/src/||' ROOTFilePB.pb.cc fastHadd.cc
g++ -O2 -o %i/bin/fastHadd ROOTFilePB.pb.cc ./fastHadd.cc \
      -I$PROTOBUF_ROOT/include -L$PROTOBUF_ROOT/lib -lprotobuf \
      `root-config --cflags --libs`

(echo "#!/bin/sh"; \
 echo "source $ROOT_ROOT/etc/profile.d/init.sh"; \
 echo "source $PROTOBUF_ROOT/etc/profile.d/init.sh"; \
 echo "source $XZ_ROOT/etc/profile.d/init.sh"; \
 echo "source $ZLIB_ROOT/etc/profile.d/init.sh"; \
 echo "source $GCC_ROOT/etc/profile.d/init.sh"; \
 echo "source $PCRE_ROOT/etc/profile.d/init.sh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PROTOBUF_ROOT/etc/profile.d/init.csh"; \
 echo "source $ROOT_ROOT/etc/profile.d/init.csh"; \
 echo "source $XZ_ROOT/etc/profile.d/init.csh"; \
 echo "source $ZLIB_ROOT/etc/profile.d/init.csh"; \
 echo "source $GCC_ROOT/etc/profile.d/init.csh"; \
 echo "source $PCRE_ROOT/etc/profile.d/init.csh"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

%install
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
