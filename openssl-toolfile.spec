### RPM external openssl-toolfile 1.0
Requires: openssl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/openssl.xml
  <tool name="openssl" version="@TOOL_VERSION@">
    <lib name="ssl"/>
    <lib name="crypto"/>
    <client>
      <environment name="OPENSSL_BASE" default="@TOOL_ROOT@"/>
      <environment name="INCLUDE" default="$OPENSSL_BASE/include"/>
      <environment name="LIBDIR" default="$OPENSSL_BASE/lib"/>
    </client>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
