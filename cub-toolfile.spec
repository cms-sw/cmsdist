### RPM external cub-toolfile 1.0
Requires: cub

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cub.xml
<tool name="cub" version="@TOOL_VERSION@">
  <use name="cuda"/>
  <client>
    <environment name="CUB_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"  default="$CUB_BASE/include"/>
  </client>
  <flags CXXFLAGS="-DCUB_STDERR"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
