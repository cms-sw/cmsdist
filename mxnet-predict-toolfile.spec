### RPM external mxnet-predict-toolfile 1.2.1.mod3
Requires: mxnet-predict
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/mxnet-predict.xml
<tool name="mxnet-predict" version="@TOOL_VERSION@">
  <lib name="mxnetpredict"/>
  <client>
    <environment name="MXNET_PREDICT_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$MXNET_PREDICT_BASE/include"/>
    <environment name="LIBDIR" default="$MXNET_PREDICT_BASE/lib"/>
  </client>
  <use name="openblas"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
