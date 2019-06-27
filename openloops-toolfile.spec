### RPM external openloops-toolfile 1.0
Requires: openloops
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/openloops.xml
<tool name="openloops" version="@TOOL_VERSION@">
<client>
<environment name="OPENLOOPS_BASE" default="@TOOL_ROOT@"/>
<environment name="LIBDIR" default="$OPENLOOPS_BASE/lib"/>
<runtime name="CMS_OPENLOOPS_PREFIX" value="$OPENLOOPS_BASE" type="path"/>
</client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
