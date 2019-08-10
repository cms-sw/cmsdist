### RPM external mxnet-predict-toolfile 1.5.0
Requires: mxnet-predict
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/mxnet-predict.xml
<tool name="mxnet-predict" version="@TOOL_VERSION@">
  <lib name="mxnet"/>
  <client>
    <environment name="MXNET_PREDICT_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$MXNET_PREDICT_BASE/include"/>
    <environment name="LIBDIR" default="$MXNET_PREDICT_BASE/lib64"/>
  </client>
  <use name="openblas"/>
  <use name="lapack"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
