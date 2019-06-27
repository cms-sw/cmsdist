### RPM external gbl-toolfile 1.0
Requires: gbl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gbl.xml
<tool name="gbl" version="@TOOL_VERSION@">
  <info url="https://www.wiki.terascale.de/index.php/GeneralBrokenLines"/>
  <lib name="GBL"/>
  <client>
    <environment name="GBL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GBL_BASE/lib"/>
    <environment name="INCLUDE" default="$GBL_BASE/include"/>
  </client>
  <use name="eigen"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
