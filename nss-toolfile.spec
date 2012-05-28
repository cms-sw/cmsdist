### RPM external nss-toolfile 1.0
Requires: nss
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/nss.xml
  <tool name="nss" version="@TOOL_VERSION@">
    <lib name="freebl3"/>
    <lib name="nss3"/>
    <lib name="nssckbi"/>
    <lib name="nssdbm3"/>
    <lib name="nsssysinit"/>
    <lib name="nssutil3"/>
    <lib name="smime3"/>
    <lib name="smime3"/>
    <lib name="ssl3"/>
    <client>
      <environment name="NSS_BASE" default="@TOOL_ROOT@"/>
      <environment name="INCLUDE" default="$NSS_BASE/include"/>
      <environment name="LIBDIR" default="$NSS_BASE/lib"/>
    </client>
    <use name="sqlite"/>
    <use name="zlib"/>
    <use name="nspr"/>
  </tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
