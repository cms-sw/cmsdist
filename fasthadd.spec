### RPM external fasthadd 2.4

#Change the commit hash every time a new version is needed.
%define commit 003102d8516b652d80e76d8ca1c4b5dc47c9015b
%define user iarspider
Source0: https://raw.githubusercontent.com/%user/cmssw/%commit/DQMServices/Components/bin/fastHadd.cc
Source1: https://raw.githubusercontent.com/%user/cmssw/%commit/DQMServices/Core/src/ROOTFilePB.proto
Requires: protobuf root abseil-cpp

%prep

%build
mkdir -p %i/bin %i/etc/profile.d

cp %{_sourcedir}/fastHadd.cc .
cp %{_sourcedir}/ROOTFilePB.proto .
protoc -I ./ --cpp_out=./ ROOTFilePB.proto
perl -p -i -e 's|DQMServices/Core/interface/||' ROOTFilePB.pb.cc fastHadd.cc
g++ -O2 -o %i/bin/fastHadd ROOTFilePB.pb.cc ./fastHadd.cc \
      -I$PROTOBUF_ROOT/include -L$PROTOBUF_ROOT/lib -lprotobuf -L$ABSEIL_CPP_ROOT/lib -labsl_log_internal_check_op \
      -labsl_log_internal_message \
      `root-config --cflags --libs`

%install
