### RPM external alpaka-toolfile 1.0
Requires: alpaka

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/alpaka.xml
<tool name="alpaka" version="@TOOL_VERSION@">
  <use name="boost"/>
  <client>
    <environment name="ALPAKA_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"     default="$ALPAKA_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/alpaka-serial.xml
<tool name="alpaka-serial" version="@TOOL_VERSION@">
  <use name="alpaka"/>
  <flags CXXFLAGS="-DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/alpaka-tbb.xml
<tool name="alpaka-tbb" version="@TOOL_VERSION@">
  <use name="alpaka"/>
  <use name="tbb"/>
  <flags CXXFLAGS="-DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/alpaka-cuda.xml
<tool name="alpaka-cuda" version="@TOOL_VERSION@">
  <use name="alpaka"/>
  <use name="cuda"/>
  <flags CXXFLAGS="-DALPAKA_ACC_GPU_CUDA_ENABLED"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
