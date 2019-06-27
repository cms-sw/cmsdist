### RPM external libxslt-toolfile 1.0
Requires: libxslt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/libxslt.xml
<tool name="libxslt" version="@TOOL_VERSION@">
  <info url="http://xmlsoft.org/libxslt"/>
  <lib name="xslt"/>
  <client>
    <environment name="LIBXSLT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$LIBXSLT_BASE/lib"/>
    <environment name="INCLUDE" default="$LIBXSLT_BASE/include/libxslt"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
