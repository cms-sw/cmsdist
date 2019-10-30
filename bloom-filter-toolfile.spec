### RPM external bloom-filter-toolfile 1.0
Requires: bloom-filter
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/bloom-filter.xml
<tool name="bloom-filter" version="@TOOL_VERSION@">
  <client>
    <environment name="BLOOM_FILTER_BASE"   default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$BF_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
