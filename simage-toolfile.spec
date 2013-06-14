### RPM external simage-toolfile 1.0
Requires: simage
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/simage.xml
<tool name="simage" version="@TOOL_VERSION@">
  <info url="http://www.coin3d.org/Coin3D/file_format_libs/simage"/>
  <lib name="simage"/>
  <client>
    <environment name="SIMAGE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$SIMAGE_BASE/lib"/>
    <environment name="INCLUDE" default="$SIMAGE_BASE/include"/>
  </client>
  <use name="zlib"/>
  <use name="libjpg"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
