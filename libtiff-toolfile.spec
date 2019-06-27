### RPM external libtiff-toolfile 1.0
Requires: libtiff
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libtiff.xml
<tool name="libtiff" version="@TOOL_VERSION@">
  <info url="http://www.libtiff.org/"/>
  <lib name="tiff"/>
  <client>
    <environment name="LIBTIFF_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBTIFF_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBTIFF_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="libjpeg-turbo"/>
  <use name="zlib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
