### RPM external mkfit-toolfile 2.0.0
Requires: mkfit

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/mkfit.xml
<tool name="mkfit" version="@TOOL_VERSION@">
  <lib name="MicCore"/>
  <lib name="MkFit"/>
  <client>
    <environment name="MKFITBASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$MKFITBASE/include"/>
    <environment name="LIBDIR" default="$MKFITBASE/lib"/>
  </client>
  <use name="tbb"/>
  <runtime name="MKFIT_BASE" value="$MKFITBASE"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
