### RPM external openssl-toolfile 1.0
%prep
%build
%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/openssl.xml
  <tool name="openssl" version="system">
    <lib name="ssl"/>
    <lib name="crypto"/>
  </tool>
EOF_TOOLFILE
