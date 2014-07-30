### RPM external fasthadd 1.0

%define tag 743bde9939bbc4f34c2b4fd022cfb980314f912a
Source0: https://raw.githubusercontent.com/cms-sw/cmssw/%tag/DQMServices/Components/bin/fastHadd.cc
Source1: https://raw.githubusercontent.com/cms-sw/cmssw/%tag/DQMServices/Core/src/ROOTFilePB.proto
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
