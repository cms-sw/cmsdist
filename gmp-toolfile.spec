### RPM external gmp-toolfile 1.0
Requires: gmp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gmp.xml
<tool name="gmp" version="@TOOL_VERSION@">
  <lib name="gmp"/>
  <client>
    <environment name="GMP_BASE"  default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"   default="$GMP_BASE/include"/>
    <environment name="LIBDIR"    default="$GMP_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
