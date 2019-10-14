### RPM external fasthadd 2.3

#Change the commit hash every time a new version is needed.
%define commit 905af02d3369428df677c232537da6fca8982ff3
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

%install
