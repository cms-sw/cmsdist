### RPM external fasthadd 1.0

%define tag 743bde9939bbc4f34c2b4fd022cfb980314f912a
Source0: https://raw.githubusercontent.com/cms-sw/cmssw/%tag/DQMServices/Components/bin/fastHadd.cc
Source1: https://raw.githubusercontent.com/cms-sw/cmssw/%tag/DQMServices/Core/src/ROOTFilePB.proto
Requires: protobuf root

%prep

%build
mkdir -p %i/bin
protoc -I ./ --cpp_out=./ %{_sourcedir}/ROOTFilePB.proto
g++ -O2 -o %i/bin ROOTFilePB.pb.cc %{_sourcedir}/fastHadd.cc -L$PROTOBUF_ROOT -lprotobuf `root-config --cflags --libs`

%install
