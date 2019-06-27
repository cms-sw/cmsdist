### RPM external cuda-api-wrappers-toolfile 2.1
Requires: cuda-api-wrappers

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cuda-api-wrappers.xml
<tool name="cuda-api-wrappers" version="@TOOL_VERSION@">
  <lib name="cuda-api-wrappers"/>
  <use name="cuda"/>
  <flags CXXFLAGS="-DCUDA_ENABLE_DEPRECATED"/>
  <client>
    <environment name="CUDA_API_WRAPPERS_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$CUDA_API_WRAPPERS_BASE/include"/>
    <environment name="LIBDIR" default="$CUDA_API_WRAPPERS_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
