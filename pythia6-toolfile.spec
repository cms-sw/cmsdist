### RPM external pythia6-toolfile 1.0
Requires: pythia6
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pythia6.xml
<tool name="pythia6" version="@TOOL_VERSION@">
  <lib name="pythia6"/>
  <lib name="pythia6_dummy"/>
  <lib name="pythia6_pdfdummy"/>
  <client>
    <environment name="PYTHIA6_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PYTHIA6_BASE/lib"/>
  </client>
  <use name="pythia6_headers"/>
  <use name="f77compiler"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/pythia6_headers.xml
<tool name="pythia6_headers" version="@TOOL_VERSION@">
  <client>
    <environment name="PYTHIA6_HEADERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PYTHIA6_HEADERS_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

