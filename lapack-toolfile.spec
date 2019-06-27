### RPM external lapack-toolfile 1.0
Requires: lapack
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/lapack.xml
<tool name="lapack" version="@TOOL_VERSION@">
  <client>
    <environment name="LAPACK_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LAPACK_BASE/lib64"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
