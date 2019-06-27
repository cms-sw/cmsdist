### RPM external libffi-toolfile 1.0
Requires: libffi
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/libffi.xml
<tool name="libffi" version="@TOOL_VERSION@">
  <lib name="ffi"/>
  <client>
    <environment name="LIBFFI_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBFFI_BASE/lib64"/>
    <environment name="INCLUDE" default="$LIBFFI_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
