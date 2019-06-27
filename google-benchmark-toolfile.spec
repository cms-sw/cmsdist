### RPM external google-benchmark-toolfile 1.0
Requires: google-benchmark
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/google-benchmark.xml
<tool name="google-benchmark" version="@TOOL_VERSION@">
  <info url="https://github.com/google/benchmark"/>
  <lib name="benchmark"/>
  <client>
    <environment name="GOOGLE_BENCHMARK_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"       default="$GOOGLE_BENCHMARK_BASE/lib"/>
    <environment name="INCLUDE"      default="$GOOGLE_BENCHMARK_BASE/include"/>
  </client>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/google-benchmark-main.xml
<tool name="google-benchmark-main" version="@TOOL_VERSION@">
  <info url="https://github.com/google/benchmark"/>
  <lib name="benchmark_main"/>
  <use name="google-benchmark"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
