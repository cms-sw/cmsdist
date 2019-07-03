### RPM external eigen-toolfile 1.0
Requires: eigen
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/eigen.xml
<tool name="eigen" version="@TOOL_VERSION@">
  <client>
    <environment name="EIGEN_BASE"   default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$EIGEN_BASE/include/eigen3"/>
  </client>
  <flags CPPDEFINES="EIGEN_DONT_PARALLELIZE"/>
  <flags CPPDEFINES="EIGEN_MPL2_ONLY"/>
  <flags CPPDEFINES="EIGEN_MAX_ALIGN_BYTES=64"/>
  <flags CPPDEFINES="EIGEN_HAS_TYPE_TRAITS=0"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
