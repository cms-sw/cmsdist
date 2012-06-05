### RPM external cyrus-sasl-toolfile 1.0
Requires: cyrus-sasl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cyrus-sasl.xml
  <tool name="cyrus-sasl" version="@TOOL_VERSION@">
    <lib name="libsasl2"/>
    <client>
      <environment name="CYRUS_SASL_BASE" default="@TOOL_ROOT@"/>
      <environment name="INCLUDE" default="$CYRUS_SASL_BASE/include"/>
      <environment name="LIBDIR" default="$CYRUS_SASL_BASE/lib"/>
    </client>
    <use name="openssl"/>
    <use name="nss"/>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
