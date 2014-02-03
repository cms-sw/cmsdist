### RPM external fastjet-contrib-toolfile 1.0
Requires: fastjet-contrib
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/fastjet-contrib.xml
  <tool name="fastjet-contrib" version="@TOOL_VERSION@">
    <info url="http://fastjet.hepforge.org/contrib/"/>
    <lib name="fastjetcontribfragile"/>
    <client>
      <environment name="FASTJET_CONTRIB_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$FASTJET_CONTRIB_BASE/lib"/>
    </client>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
