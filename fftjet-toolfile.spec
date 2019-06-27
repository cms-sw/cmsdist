### RPM external fftjet-toolfile 1.0
Requires: fftjet
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/fftjet.xml
<tool name="fftjet" version="@TOOL_VERSION@">
  <lib name="fftjet"/>
  <client>
    <environment name="FFTJET_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$FFTJET_BASE/lib"/>
    <environment name="INCLUDE" default="$FFTJET_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post

# bla bla
