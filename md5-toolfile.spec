### RPM external md5-toolfile 1.0
Requires: md5

%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/md5.xml
<tool name="md5" version="@TOOL_VERSION@">
  <info url="https://tls.mbed.org/md5-source-code"/>
   <lib name="cms-md5"/>
  <client>
    <environment name="MD5_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$MD5_BASE/lib"/>
    <environment name="INCLUDE" default="$MD5_BASE/include"/>
    </client>  
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
