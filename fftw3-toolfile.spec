### RPM external fftw3-toolfile 1.0
Requires: fftw3
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/fftw3.xml
<tool name="fftw3" version="@TOOL_VERSION@">
  <lib name="fftw3"/>
  <client>
    <environment name="FFTW3_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$FFTW3_BASE/include"/>
    <environment name="LIBDIR" default="$FFTW3_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
