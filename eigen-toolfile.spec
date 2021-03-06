### RPM external eigen-toolfile 2.0
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
  <runtime name="ROOT_INCLUDE_PATH"  value="$INCLUDE" type="path"/>
  <flags CPPDEFINES="EIGEN_DONT_PARALLELIZE"/>
  <flags CUDA_FLAGS="--diag-suppress 20014"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
