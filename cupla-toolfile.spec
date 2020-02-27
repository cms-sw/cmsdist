### RPM external cupla-toolfile 1.0
Requires: cupla

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cupla.xml
<tool name="cupla" version="@TOOL_VERSION@">
  <info url="https://github.com/ComputationalRadiationPhysics/cupla"/>
  <use name="boost"/>
  <client>
    <environment name="CUPLA_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"    default="$CUPLA_BASE/include"/>
    <environment name="LIBDIR"     default="$CUPLA_BASE/lib"/>
  </client>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/cupla-serial.xml
<tool name="cupla-serial" version="@TOOL_VERSION@">
  <use name="cupla"/>
  <lib name="cupla-serial"/>
  <flags CXXFLAGS="-DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=0"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/cupla-tbb.xml
<tool name="cupla-tbb" version="@TOOL_VERSION@">
  <use name="cupla"/>
  <use name="tbb"/>
  <lib name="cupla-tbb"/>
  <flags CXXFLAGS="-DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/cupla-cuda.xml
<tool name="cupla-cuda" version="@TOOL_VERSION@">
  <use name="cupla"/>
  <use name="cuda"/>
  <lib name="cupla-cuda"/>
  <flags CXXFLAGS="-DALPAKA_ACC_GPU_CUDA_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
