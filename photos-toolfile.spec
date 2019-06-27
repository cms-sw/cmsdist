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
  </client>
  <use name="photos_headers"/>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/photos_headers.xml
<tool name="photos_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="PHOTOS_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PHOTOS_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
