### RPM external form-toolfile 1.0
Requires: form
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/form.xml
<tool name="form" version="@TOOL_VERSION@">
  <client>
    <environment name="FORM_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$FORM_BASE/bin"/>
  </client>
  <runtime name="PATH" default="$BINDIR" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

