### RPM external mpfr-static-toolfile 1.0
Requires: mpfr-static
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/mpfr.xml
<tool name="mpfr" version="@TOOL_VERSION@">
  <lib name="mpfr"/>
  <client>
    <environment name="MPFR_BASE"  default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"   default="$MPFR_BASE/include"/>
    <environment name="LIBDIR"    default="$MPFR_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
