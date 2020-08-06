### RPM external hdf5-toolfile 1.0
Requires: hdf5
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/hdf5.xml
<tool name="hdf5" version="@TOOL_VERSION@">
  <info url="https://support.hdfgroup.org/HDF5/"/>
  <lib name="hdf5"/>
  <client>
    <environment name="HDF5_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$HDF5_BASE/lib"/>
    <environment name="INCLUDE" default="$HDF5_BASE/include"/>
  </client>
  <use name="openmpi"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
