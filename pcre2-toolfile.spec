### RPM external pcr2-toolfile 1.0
Requires: pcre2
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/pcre2.xml
<tool name="pcre2" version="@TOOL_VERSION@">
  <info url="http://www.pcre.org"/>
  <lib name="pcre2"/>
  <client>
    <environment name="PCRE2_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PCRE2_BASE/lib"/>
    <environment name="INCLUDE" default="$PCRE2_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="bz2lib"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
