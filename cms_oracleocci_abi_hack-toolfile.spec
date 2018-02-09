### RPM cms cms_oracleocci_abi_hack-toolfile 1.0
Requires: cms_oracleocci_abi_hack
%prep

%build

%install

mkdir -p %i/etc/scram.d
if ${CMS_ORACLEOCCI_ABI_HACK_ROOT}/bin/is_cxx11_abi ; then
cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci.xml
<tool name="oracleocci" version="@TOOL_VERSION@">
  <lib name="cms_oracleocci_abi_hack"/>
  <use name="oracleocci-official"/>
  <client>
    <environment name="ORACLEOCCI_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" value="$ORACLEOCCI_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE
else
cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci.xml
<tool name="oracleocci" version="@TOOL_VERSION@">
  <use name="oracleocci-official"/>
</tool>
EOF_TOOLFILE
fi

## IMPORT scram-tools-post
