### RPM external h5cpp-toolfile 1.0
Requires: h5cpp
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/h5cpp.xml
<tool name="hdf5" version="@TOOL_VERSION@">
  <info url="https://github.com/ess-dmsc/h5cpp"/>
  <lib name="h5cpp"/>
  <client>
    <environment name="H5CPP_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$H5CPP_BASE/lib"/>
    <environment name="INCLUDE" default="$H5CPP_BASE/include"/>
  </client>
  <use name="hdf5"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
