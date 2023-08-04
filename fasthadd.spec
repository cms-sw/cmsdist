### RPM external fasthadd 2.4

#Change the commit hash every time a new version is needed.
%define commit 972d35c43d210761a9fa31ff6c53490a615a383b
%define user cms-sw
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
