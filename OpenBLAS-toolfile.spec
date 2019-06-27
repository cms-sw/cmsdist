### RPM external OpenBLAS-toolfile 1.0
Requires: OpenBLAS
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/OpenBLAS.xml
<tool name="OpenBLAS" version="@TOOL_VERSION@">
  <lib name="openblas"/>
  <client>
    <environment name="OPENBLAS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$OPENBLAS_BASE/include"/>
    <environment name="LIBDIR" default="$OPENBLAS_BASE/lib"/>
    <environment name="BINDIR" default="$OPENBLAS_BASE/bin"/>
  </client>
  <runtime name="OPENBLAS_NUM_THREADS" value="1"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
