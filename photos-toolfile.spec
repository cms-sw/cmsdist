### RPM external photos-toolfile 1.0
Requires: photos
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/photos.xml
<tool name="photos" version="@TOOL_VERSION@">
  <lib name="photos"/>
  <client>
    <environment name="PHOTOS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PHOTOS_BASE/lib"/>
    <environment name="INCLUDE" default="$PHOTOS_BASE/include"/>
  </client>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
