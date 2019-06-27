### RPM external doxygen-toolfile 1.0
Requires: doxygen

%prep
%build
%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE > %{i}/etc/scram.d/doxygen.xml
  <tool name="doxygen" version="@TOOL_VERSION@">
    <info url="http://www.stack.nl/~dimitri/doxygen/"/>
    <client>
      <environment name="DOXYGEN_BASE" default="@TOOL_ROOT@"/>
    </client>
    <runtime name="PATH" value="$DOXYGEN_BASE/bin" type="path"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
