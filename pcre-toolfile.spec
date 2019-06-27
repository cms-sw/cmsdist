### RPM external pcre-toolfile 1.0
Requires: pcre
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/pcre.xml
<tool name="pcre" version="@TOOL_VERSION@">
  <info url="http://www.pcre.org"/>
  <lib name="pcre"/>
  <client>
    <environment name="PCRE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PCRE_BASE/lib"/>
    <environment name="INCLUDE" default="$PCRE_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="bz2lib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
