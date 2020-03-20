### RPM external pythia6-toolfile 2.1
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
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/pydata.xml
<tool name="pydata" version="@TOOL_VERSION@">
  <client>
    <environment name="PYDATA_BASE" default="@TOOL_ROOT@"/>
  </client>
  <architecture name="slc.*|fc.*|cc*">
    <flags LDFLAGS="$(PYDATA_BASE)/lib/pydata.o"/>
  </architecture>
  <flags NO_RECURSIVE_EXPORT="1"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

