### RPM external libpng-toolfile 1.0
Requires: libpng
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libpng.xml
<tool name="libpng" version="@TOOL_VERSION@">
  <info url="http://www.libpng.org/"/>
  <lib name="png"/>
  <client>
    <environment name="LIBPNG_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBPNG_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBPNG_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
