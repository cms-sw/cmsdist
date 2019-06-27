### RPM external sip-toolfile 1.0
Requires: sip
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/sip.xml
<tool name="sip" version="@TOOL_VERSION@">
  <info url="http://www.riverbankcomputing.co.uk/software/sip/intro"/>
  <client>
    <environment name="SIP_BASE" default="@TOOL_ROOT@"/>
  </client>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
# bla bla
