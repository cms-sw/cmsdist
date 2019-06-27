### RPM external davix-toolfile 1.1
Requires: davix

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE > %i/etc/scram.d/davix.xml
  <tool name="davix" version="@TOOL_VERSION@">
    <info url="https://dmc.web.cern.ch/projects/davix/home"/>
    <lib name="davix"/>
    <client>
      <environment name="DAVIX_BASE" default="@TOOL_ROOT@"/>
      <environment name="LIBDIR" default="$DAVIX_BASE/lib64"/>
      <environment name="INCLUDE" default="$DAVIX_BASE/include/davix"/>
    </client>
    <runtime name="PATH" value="$DAVIX_BASE/bin" type="path"/>
    <use name="boost_system"/>
    <use name="openssl"/>
    <use name="libxml2"/>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
