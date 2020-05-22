### RPM external opencv-toolfile 1.0
Requires: opencv
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/opencv.xml
<tool name="opencv" version="@TOOL_VERSION@">
  <lib name="opencv_core"/>
  <client>
    <environment name="OPENCV_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$OPENCV_BASE/include"/>
    <environment name="LIBDIR" default="$OPENCV_BASE/lib"/>
    <environment name="BINDIR" default="$OPENCV_BASE/bin"/>
  </client>
  <use name="libpng"/>
  <use name="libjpeg-turbo"/>
  <use name="zlib"/>
  <use name="eigen"/>
  <use name="OpenBLAS"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
